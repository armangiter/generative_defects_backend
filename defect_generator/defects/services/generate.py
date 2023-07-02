import logging, os
from pathlib import Path

from django.core.files import File
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache

import requests
from defect_generator.defects.exceptions import AlreadyGeneratingError

from defect_generator.defects.models import DefectModel, DefectType, Result
from defect_generator.defects.tasks.generate import generate as generate_task
from defect_generator.defects.utils import (
    get_real_url,
    write_file_to_disk,
)


logger = logging.getLogger(__name__)


class GenerateService:
    @staticmethod
    def get_generate_status() -> str:
        response = "generating" if cache.get("generate-lock") else "ready"
        return response

    @staticmethod
    def finish_generate() -> str:
        # release the lock
        cache.set("generate-lock", False)

    @staticmethod
    def generate(
        *,
        user,
        image_file: File,
        mask_file: File,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
    ) -> None:
        # lock = cache.get("generate-lock")
        # if lock:
        #     return False

        # # lock the generate
        # cache.set("generate-lock", True)

        generating_result_exists = Result.objects.filter(
            status=Result.STATUS_GENERATING
        ).exists()
        if generating_result_exists:
            raise AlreadyGeneratingError(
                {"message": "there is a generate task running already."}
            )

        file_path = write_file_to_disk(file=image_file)
        mask_file_path = write_file_to_disk(file=mask_file)

        generate_task.delay(
            file_path,
            mask_file_path,
            defect_type_id,
            defect_model_id,
            mask_mode,
            number_of_images,
            user.id,
        )

        return True


class GenerateCeleryService:
    @staticmethod
    @transaction.atomic
    def generate(
        *,
        file_path: str,
        mask_file_path: str,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
        user_id: int,
    ) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)
        mask_path_object = Path(mask_file_path)

        with file_path_object.open(mode="rb") as file, mask_path_object.open(
            mode="rb"
        ) as mask_file:
            logger.info(f"Uploading file: {file.name} ....")

            image_file = File(file, name=file.name)
            mask_image_file = File(mask_file, name=mask_file.name)

            defect_model = DefectModel.objects.get(id=defect_model_id)
            defect_type = (
                DefectType.objects.filter(id=defect_type_id).only("command").get()
            )

            result = Result.objects.create(
                defect_model=defect_model,
                defect_type=defect_type,
                user_id=user_id,
                status=Result.STATUS_PENDING,
            )

            requests.post(
                "http://inference_web:8000/inference/",
                data={
                    "model_url": defect_model.file.url,
                    "number_of_images": number_of_images,
                    "defect_type_id": defect_type_id,
                    "defect_model_id": defect_model_id,
                    "instance_prompt": defect_type.command,
                    "result_id": result.id,
                },
                files={"image_file": image_file, "mask_file": mask_image_file},
            )
            # create a Result with pending status
            result.image = image_file
            result.save(update_fields=["image"])

            storage.delete(image_file.name)
            storage.delete(mask_image_file.name)
