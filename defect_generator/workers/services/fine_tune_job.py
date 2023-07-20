import logging
from pathlib import Path

from django.db import transaction
from django.db.models import F
from django.contrib.auth import get_user_model
from rest_framework import exceptions

import requests

from defect_generator.common.services import model_update
from defect_generator.defects.exceptions import AlreadyGeneratingError

from defect_generator.defects.models import (
    FineTune,
    FineTuneImage,
    Image,
)

logger = logging.getLogger(__name__)
User = get_user_model()


class FineTuneJobService:
    @transaction.atomic
    @staticmethod
    def get_earliest_fine_tune_job(*, filters=None) -> None:
        pending_fine_tune = (
            FineTune.objects.filter(status=FineTune.STATUS_PENDING)
            .select_for_update()
            .order_by("created")
            .first()
        )
        if pending_fine_tune is None:
            raise exceptions.NotFound({"message": "there is no pending fine tune job."})

        # creating FineTuneImage instances for each not tuned Image
        images_id = Image.objects.filter(tuned=False).values_list("id", flat=True)
        fine_tune_images = [
            FineTuneImage(fine_tune=pending_fine_tune, image_id=image_id)
            for image_id in images_id
        ]
        FineTuneImage.objects.bulk_create(fine_tune_images)

        generating_fine_tune, updated = model_update(
            instance=pending_fine_tune,
            fields=["status"],
            data={"status": FineTune.STATUS_GENERATING},
        )
        return generating_fine_tune
