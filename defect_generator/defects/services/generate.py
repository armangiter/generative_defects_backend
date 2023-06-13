import logging, os
from pathlib import Path

from django.core.files import File
from django.core.files.storage import FileSystemStorage
import requests

import PIL

from defect_generator.defects.models import DefectModel, DefectType
from defect_generator.defects.tasks.generate import generate as generate_task
from defect_generator.defects.utils import (
    get_real_url,
    write_file_to_disk,
)


logger = logging.getLogger(__name__)


class GenerateService:
    @staticmethod
    def get_generate_status() -> str:
        response = requests.get("http://inference_web:8000/status").json()
        return response["status"]

    @staticmethod
    def generate(
        *,
        image_file: File,
        mask_file: File,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
    ) -> None:
        file_path = write_file_to_disk(file=image_file)
        mask_file_path = write_file_to_disk(file=mask_file)

        generate_task.delay(
            file_path,
            mask_file_path,
            defect_type_id,
            defect_model_id,
            mask_mode,
            number_of_images,
        )


class GenerateCeleryService:
    @staticmethod
    def generate(
        *,
        file_path: str,
        mask_file_path: str,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
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
                DefectType.objects.filter(id=defect_type_id).only("name").get()
            )

            # model_url = get_real_url(defect_model.file.url)

            requests.post(
                "http://inference_web:8000/inference/",
                data={
                    "model_url": defect_model.file.url,
                    "number_of_images": number_of_images,
                    "defect_type_id": defect_type_id,
                    "defect_model_id": defect_model_id,
                    "defect_type_name": defect_type.name,
                },
                files={"image_file": image_file, "mask_file": mask_image_file},
            )

            storage.delete(image_file.name)
            storage.delete(mask_image_file.name)
