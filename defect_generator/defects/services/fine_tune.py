import logging, os
from pathlib import Path

from django.db import transaction
from django.db.models import QuerySet
from defect_generator.defects.filters import FineTuneFilter

from defect_generator.defects.models import FineTune, Image


logger = logging.getLogger(__name__)


class FineTuneService:
    @staticmethod
    @transaction.atomic
    def fine_tune_create(user) -> None:
        FineTune.objects.create(
            user_id=user.id,
            status=FineTune.STATUS_PENDING,
        )

    @staticmethod
    def fine_tune_list(*, user, filters=None) -> QuerySet[FineTune]:
        queryset = FineTune.objects.order_by("-id").filter(user=user)

        if filters is None:
            filters = {}

        return FineTuneFilter(filters, queryset=queryset).qs

    @staticmethod
    def fine_tune_update(
        *,
        fine_tune_id: int,
        status: str,
    ) -> None:
        FineTune.objects.filter(id=fine_tune_id).update(status=status)

    @staticmethod
    def fine_tune_get(*, fine_tune_id: int, filters=None) -> FineTune:
        return FineTune.objects.get(id=fine_tune_id)

    @staticmethod
    def fine_tune_delete(*, fine_tune_id: int) -> None:
        FineTune.objects.filter(id=fine_tune_id).delete()

    @staticmethod
    def get_related_images(fine_tune: FineTune) -> QuerySet[Image]:
        fine_tune_images_id = fine_tune.fine_tune_images.all().values_list(
            "image_id", flat=True
        )
        return Image.objects.filter(id__in=fine_tune_images_id)
