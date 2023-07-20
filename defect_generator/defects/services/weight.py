import logging
from pathlib import Path

from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage


from defect_generator.defects.models import Weight
from defect_generator.defects.tasks.weight import upload_weight as upload_weight_task
from defect_generator.defects.utils import write_file_to_disk


logger = logging.getLogger(__name__)


class WeightService:
    @staticmethod
    def weight_create(*, file: File) -> None:
        # Writing image and mask on the disk (Temporarily)
        file_path = write_file_to_disk(file=file)

        # Calling the celery task
        upload_weight_task.delay(
            file_path,
            file.name,
        )

    @staticmethod
    def weight_list(*, filters=None) -> QuerySet[Weight]:
        return Weight.objects.all()

    @staticmethod
    def weight_get(*, weight_id: int, filters=None) -> Weight:
        return Weight.objects.get(id=weight_id)

    @staticmethod
    def weight_delete(*, weight_id: int) -> None:
        Weight.objects.filter(id=weight_id).delete(id=weight_id)


class WeightCeleryService:
    @staticmethod
    def weight_create(*, file_path: str, file_name: str) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)

        with file_path_object.open(mode="rb") as file:
            logger.info(f"Uploading file: {file.name} ....")

            weight_file = File(file, name=file.name)

            Weight.objects.create(file=weight_file)

        storage.delete(file_name)
