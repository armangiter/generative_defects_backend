import logging
from pathlib import Path

from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import exceptions

import requests

from defect_generator.common.services import model_update
from defect_generator.defects.exceptions import AlreadyGeneratingError

from defect_generator.defects.models import DefectModel, DefectType, Result
from defect_generator.defects.serializers.generate import GenerateInputSerializer
from defect_generator.defects.tasks.generate import generate as generate_task
from defect_generator.defects.utils import (
    get_real_url,
    write_file_to_disk,
)


logger = logging.getLogger(__name__)
User = get_user_model()


class GenerateJobService:
    @staticmethod
    def get_earliest_generate_job(*, filters=None) -> None:
        pending_result = (
            Result.objects.filter(status=Result.STATUS_PENDING)
            .order_by("created")
            .first()
        )
        if pending_result is None:
            raise exceptions.NotFound({"message": "there is no pending job."})

        generating_result, updated = model_update(
            instance=pending_result,
            fields=["status"],
            data={"status": Result.STATUS_GENERATING},
        )
        return generating_result
