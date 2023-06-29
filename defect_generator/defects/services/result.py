import logging
from pathlib import Path

from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage


from defect_generator.defects.models import Result, ResultImage
from defect_generator.defects.tasks.result import result_create as result_create_task
from defect_generator.defects.utils import write_file_to_disk


logger = logging.getLogger(__name__)


class ResultService:
    @staticmethod
    def result_create(
        *, image: File, defect_type_id: int, defect_model_id: int
    ) -> Result:
        file_path = write_file_to_disk(file=image)

        result = Result.objects.create(
            defect_type_id=defect_type_id,
            defect_model_id=defect_model_id,
        )

        # calling celery task for uploading image field of result
        result_create_task.delay(file_path, image.name, result.id)
        return result

    @staticmethod
    @transaction.atomic
    def result_list(*, filters=None) -> QuerySet[Result]:
        queryset = (
            Result.objects.prefetch_related("result_images")
            .select_related("defect_type")
            .filter(used=False)
            .order_by("-id")
        )
        Result.objects.all().update(used=True)
        return queryset

    @staticmethod
    def result_get(*, id: int, filters=None) -> Result:
        return Result.objects.prefetch_related("result_images").get(id=id)

    @staticmethod
    def result_delete(*, image_id: int) -> None:
        Result.objects.filter(id=image_id).delete()


class ResultCeleryService:
    @transaction.atomic
    @staticmethod
    def result_create(*, file_path: str, file_name: str, result_id: int) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)

        with file_path_object.open(mode="rb") as file:
            logger.info(f"Uploading file: {file.name} ....")

            image_file = File(file, name=file.name)

            result = Result.objects.get(id=result_id)
            result.image = image_file
            result.save(update_fields=["image"])

        storage.delete(file_name)
