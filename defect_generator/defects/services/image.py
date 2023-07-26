import logging
from pathlib import Path
import uuid

from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from defect_generator.defects.models import Image
from defect_generator.defects.tasks.images import (
    upload_image as upload_image_task,
    update_image as update_image_task,
)
from defect_generator.defects.utils import get_file_extension, write_file_to_disk


logger = logging.getLogger(__name__)


class ImageService:
    @staticmethod
    def image_create(*, file: File, mask_file: File, defect_type_id: int) -> None:
        # Writing image and mask on the disk (Temporarily)
        file_path = write_file_to_disk(file=file)
        mask_file_path = write_file_to_disk(file=mask_file)

        # Calling the celery task
        upload_image_task.delay(
            file_path, file.name, mask_file_path, mask_file.name, defect_type_id
        )

    @staticmethod
    def image_list(*, filters=None) -> QuerySet[Image]:
        return Image.objects.filter(tuned=False)

    @staticmethod
    def image_get(*, id: int, filters=None) -> Image:
        return Image.objects.get(id=id)

    @staticmethod
    def image_update(
        *, image_id: int, file: File, mask_file: File, defect_type_id: int
    ) -> None:
        # Writing image and mask on the disk (Temporarily)
        file_path = write_file_to_disk(file=file)
        mask_file_path = write_file_to_disk(file=mask_file)

        # Calling the celery task
        update_image_task.delay(
            image_id,
            file_path,
            file.name,
            mask_file_path,
            mask_file.name,
            defect_type_id,
        )

    @staticmethod
    def image_delete(*, image_id: int) -> None:
        # TODO: Implement the deletion in the storage too
        Image.objects.filter(id=image_id).delete()


class ImageUploadService:
    @transaction.atomic
    @staticmethod
    def image_create(
        *,
        file_path: str,
        file_name: str,
        mask_file_path: str,
        mask_file_name: str,
        defect_type_id: int,
    ) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)
        mask_path_object = Path(mask_file_path)

        with file_path_object.open(mode="rb") as file, mask_path_object.open(
            mode="rb"
        ) as mask_file:
            logger.info(f"Uploading file: {file.name} ....")

            image = Image.objects.create(defect_type_id=defect_type_id)

            image_ext = get_file_extension(file_path_object.name)
            mask_ext = get_file_extension(mask_path_object.name)

            file_name = f"{str(uuid.uuid4())}.{image_ext}"
            mask_file_name = f"{str(uuid.uuid4())}.{mask_ext}"

            image_file = File(file, name=file_name)
            mask_image_file = File(mask_file, name=mask_file_name)

            # Upload the file
            image.file = image_file
            image.file.name = f"images/{file_name}"
            image.mask_file = mask_image_file
            image.mask_file.name = f"masks/{mask_file_name}"
            image.save(update_fields=["file", "mask_file"])

        storage.delete(file_name)
        storage.delete(mask_file_name)

    @transaction.atomic
    @staticmethod
    def image_update(
        *,
        image_id: int,
        file_path: str,
        file_name: str,
        mask_file_path: str,
        mask_file_name: str,
        defect_type_id: int,
    ) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)
        mask_path_object = Path(mask_file_path)

        with file_path_object.open(mode="rb") as file, mask_path_object.open(
            mode="rb"
        ) as mask_file:
            logger.info(f"Uploading file: {file.name} ....")

            image = Image.objects.get(id=image_id)

            image_ext = get_file_extension(file_path_object.name)
            mask_ext = get_file_extension(mask_path_object.name)

            image_file = File(file, name=f"{image.id}.{image_ext}")
            mask_image_file = File(mask_file, name=f"mask_{image.id}.{mask_ext}")

            # Upload the file
            image.file = image_file
            image.file.name = f"images/img_{image.id}.{image_ext}"

            image.mask_file = mask_image_file
            image.mask_file.name = f"masks/mask_{image.id}.{image_ext}"

            image.defect_type_id = defect_type_id

            image.save(update_fields=["file", "mask_file", "defect_type"])

        storage.delete(file_name)
        storage.delete(mask_file_name)
