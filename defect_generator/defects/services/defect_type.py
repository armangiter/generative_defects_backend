import logging
from pathlib import Path
import uuid

from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from defect_generator.defects.filters import DefectTypeFilter
from defect_generator.defects.models import DefectType
from defect_generator.defects.tasks.defect_type import upload_defect_type
from defect_generator.defects.utils import get_file_extension, write_file_to_disk


logger = logging.getLogger(__name__)


class DefectTypeService:
    @staticmethod
    def defect_type_create(*, name: str, command: str, icon_image: File) -> None:
        # Writing image and mask on the disk (Temporarily)
        file_path = write_file_to_disk(file=icon_image)

        defect_type = DefectType.objects.create(name=name, command=command)

        # Calling the celery task
        upload_defect_type.delay(
            file_path, icon_image.name, defect_type.id
        )

    @staticmethod
    def defect_type_list(*, filters=None) -> QuerySet[DefectType]:
        if filters is None:
            qs = DefectType.objects.filter(defect_model_id__isnull=True)
            filters = {}
        else:
            qs = DefectType.objects.filter(defect_model__isnull=False)

        return DefectTypeFilter(filters, queryset=qs).qs

    @staticmethod
    def defect_type_get(*, id: int, filters=None) -> DefectType:
        return DefectType.objects.get(id=id)

    @staticmethod
    def defect_type_update(*, type_id: int, name: str, command: str) -> None:
        DefectType.objects.filter(id=type_id).update(name=name, command=command)

    @staticmethod
    def defect_type_delete(*, type_id: int) -> None:
        DefectType.objects.filter(id=type_id).delete(id=type_id)


class DefectTypeCeleryService:
    @transaction.atomic
    @staticmethod
    def defect_type_create(
        *,
        file_path: str,
        file_name: str,
        defect_type_id: int,
    ) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)

        with file_path_object.open(mode="rb") as file:
            logger.info(f"Uploading file: {file.name} ....")

            defect_type = DefectType.objects.get(id=defect_type_id)

            ext = get_file_extension(file_path_object.name)

            file_name = f"{str(uuid.uuid4())}.{ext}"

            icon_image_file = File(file, name=file_name)

            # Upload the file
            defect_type.icon_image = icon_image_file
            defect_type.save(update_fields=["icon_image"])

        storage.delete(file_name)