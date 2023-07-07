import logging
from pathlib import Path

from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from defect_generator.common.types import DjangoModelType
from defect_generator.defects.filters import ResultFilter


from defect_generator.defects.models import Result, ResultImage
from defect_generator.defects.tasks.result import result_create as result_create_task
from defect_generator.defects.utils import write_file_to_disk


logger = logging.getLogger(__name__)


class ResultService:
    @staticmethod
    def result_create(
        *, image: File, mask: File, defect_type_id: int, defect_model_id: int
    ) -> Result:
        file_path = write_file_to_disk(file=image)
        mask_path = write_file_to_disk(file=mask)

        result = Result.objects.create(
            defect_type_id=defect_type_id,
            defect_model_id=defect_model_id,
        )

        # calling celery task for uploading image field of result
        result_create_task.delay(file_path, image.name, mask_path, mask.name, result.id)
        return result

    @staticmethod
    def result_list(*, user, filters=None) -> QuerySet[Result]:
        queryset = (
            Result.objects.prefetch_related("result_images")
            .select_related("defect_type", "defect_model")
            .order_by("-id")
            .filter(user=user)
        )

        if filters is None:
            filters = {}

        return ResultFilter(filters, queryset=queryset).qs

    @staticmethod
    def result_update(*, result_id: int, status: str) -> None:
        Result.objects.filter(id=result_id).update(status=status)

    @staticmethod
    def result_get(*, id: int, filters=None) -> Result:
        return (
            Result.objects.prefetch_related("result_images")
            .select_related("defect_type", "defect_model")
            .get(id=id)
        )

    @staticmethod
    def result_delete(*, image_id: int) -> None:
        Result.objects.filter(id=image_id).delete()


class ResultCeleryService:
    @transaction.atomic
    @staticmethod
    def result_create(
        *,
        file_path: str,
        file_name: str,
        mask_path: str,
        mask_name: str,
        result_id: int,
    ) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)
        mask_path_object = Path(mask_path)

        with file_path_object.open(mode="rb") as file, mask_path_object.open(
            mode="rb"
        ) as mask_file:
            logger.info(f"Uploading file: {file.name} ....")

            image_file = File(file, name=file.name)
            mask_image_file = File(mask_file, name=mask_file.name)

            result = Result.objects.get(id=result_id)
            result.image = image_file
            result.mask = mask_image_file
            result.save(update_fields=["image", "mask"])

        storage.delete(file_name)
        storage.delete(mask_name)
