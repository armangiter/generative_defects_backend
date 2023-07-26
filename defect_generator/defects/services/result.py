import logging
from pathlib import Path
import uuid

from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from defect_generator.common.services import model_update
from defect_generator.common.types import DjangoModelType
from defect_generator.defects.filters import ResultFilter
from rest_framework.exceptions import NotFound 

from defect_generator.defects.models import Result, ResultImage
from defect_generator.defects.tasks.result import result_create as result_create_task
from defect_generator.defects.utils import get_file_extension, write_file_to_disk


logger = logging.getLogger(__name__)


class ResultService:
    @staticmethod
    def result_create(
        *,
        user,
        image: File,
        mask: File,
        number_of_images: int,
        mask_mode: str,
        defect_type_id: int,
        defect_model_id: int,
    ) -> Result:
        file_path = write_file_to_disk(file=image)
        mask_path = write_file_to_disk(file=mask)

        result = Result.objects.create(
            user=user,
            defect_type_id=defect_type_id,
            defect_model_id=defect_model_id,
            number_of_images=number_of_images,
            mask_mode=mask_mode,
            status=Result.STATUS_PENDING,
        )

        # calling celery task for uploading image field of result
        result_create_task.delay(file_path, image.name, mask_path, mask.name, result.id)
        return result

    @staticmethod
    def result_list(*, user, filters=None) -> QuerySet[Result]:
        queryset = (
            Result.objects.prefetch_related("result_images")
            .select_related("defect_type", "defect_model", "defect_type__weight")
            .order_by("-id")
            .filter(user=user)
        )

        if filters is None:
            filters = {}

        return ResultFilter(filters, queryset=queryset).qs

    @staticmethod
    def result_update(
        *, result_id: int, data: dict) -> None:
        try:
            result = Result.objects.get(id=result_id)
        except Result.DoesNotExist:
            raise NotFound({"message", "result not found with provided id"})
        print(data)
        fields = []
        if data.get("status") is not None:
            fields.append("status")
        if data.get("error") is not None:
            fields.append("error")
        if data.get("progress") is not None:
            fields.append("progress")
        
        model_update(instance=result, fields=fields, data=data)

    @staticmethod
    def result_get(*, id: int, filters=None) -> Result:
        return (
            Result.objects.prefetch_related("result_images")
            .select_related("defect_type", "defect_model", "defect_type__weight")
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

            image_ext = get_file_extension(file_path_object.name)
            mask_ext = get_file_extension(mask_path_object.name)

            file_name = f"{str(uuid.uuid4())}.{image_ext}"
            mask_name = f"{str(uuid.uuid4())}.{mask_ext}"

            image_file = File(file, name=file_name)
            mask_image_file = File(mask_file, name=mask_name)

            result = Result.objects.get(id=result_id)
            result.image = image_file
            result.mask = mask_image_file
            result.save(update_fields=["image", "mask"])

        storage.delete(file_name)
        storage.delete(mask_name)
