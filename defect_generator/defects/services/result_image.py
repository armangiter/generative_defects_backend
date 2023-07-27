import logging
from pathlib import Path
import uuid

from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from defect_generator.defects.models import ResultImage
from defect_generator.defects.tasks.result_image import result_image_create
from defect_generator.defects.utils import get_file_extension, write_file_to_disk


logger = logging.getLogger(__name__)


class ResultImageService:
    @staticmethod
    def image_create(*, files: list[File], result_id: int) -> None:
        # Writing image and mask on the disk (Temporarily)
        files_path = []
        files_name = []
        for file in files:
            file_path = write_file_to_disk(file=file)
            files_path.append(file_path)
            files_name.append(file.name)

        print(files_path)
        print(files_name)
        # Calling the celery task
        result_image_create.delay(files_path, files_name, result_id)

    @staticmethod
    def image_list(*, filters=None) -> QuerySet[ResultImage]:
        return ResultImage.objects.all()


class ResultImageCeleryService:
    @staticmethod
    @transaction.atomic
    def image_create(
        *,
        files_path: str,
        files_name: str,
        result_id: int,
    ) -> None:
        storage = FileSystemStorage()
        result_images = []
        for file_path in files_path:
            file_path_object = Path(file_path)

            with file_path_object.open(mode="rb") as file:
                logger.info(f"Uploading file: {file.name} ....")
                ext = get_file_extension(file_path_object.name)
                file_name = f"{str(uuid.uuid4())}.{ext}"
                result_image_file = File(file, name=file_name)
                ResultImage.objects.create(result_id=result_id, file=result_image_file)

        for file_name in files_name:
            storage.delete(file_name)
