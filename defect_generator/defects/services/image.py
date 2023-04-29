import logging, os
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from defect_generator.defects.models import Image
from defect_generator.defects.tasks.images import upload_image as upload_image_task


logger = logging.getLogger(__name__)


class ImageService:
    @staticmethod
    def image_create(*, file: File, defect_type_id: int) -> None:
        # Writing image on the disk (Temporarily)
        storage = FileSystemStorage()
        logger.info(f"file name: {file.name}")
        file.name = storage.get_available_name(file)
        logger.info(f"file name after : {file.name}")
        storage.save(file.name, File(file))
        logger.info(f"Received file: {file.name}")
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        # Calling the celery task
        upload_image_task.delay(file_path, file.name, defect_type_id)

    @staticmethod
    def image_list(*, filters=None) -> QuerySet[Image]:
        return Image.objects.all()

    @staticmethod
    def image_get(*, id: int, filters=None) -> Image:
        return Image.objects.get(id=id)

    @staticmethod
    def image_delete(*, image_id: int) -> None:
        Image.objects.filter(id=image_id).delete()


class ImageUploadService:
    @transaction.atomic
    @staticmethod
    def upload_image(*, file_path: str, file_name: str, defect_type_id: int) -> None:
        storage = FileSystemStorage()
        path_object = Path(file_path)

        with path_object.open(mode="rb") as file:
            image_file = File(file, name=path_object.name)

            # Upload the file
            logger.info(f"Uploading file: {file.name} ....")
            image = Image.objects.create(file=image_file, defect_type_id=defect_type_id)

        storage.delete(file_name)
