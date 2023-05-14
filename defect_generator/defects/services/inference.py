import logging, os
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import requests
from config.env import BASE_DIR

import PIL

from defect_generator.defects.models import Image, DefectModel, DefectType
from defect_generator.defects.tasks.inference import inference as inference_task
from defect_generator.defects.utils import download_file, get_real_url


logger = logging.getLogger(__name__)


class InferenceService:
    @staticmethod
    def inference(
        *,
        image_file: File,
        mask_file: File,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
    ) -> None:
        defect_model = DefectModel.objects.get(id=defect_model_id)
        defect_type = DefectType.objects.get(id=defect_type_id)

        model_url = get_real_url(defect_model.file.url)
        
        requests.post(
            "http://inference_web:8000/inference/",
            data={
                "model_url": model_url,
                "number_of_images": number_of_images,
            },
            files={"image_file": image_file, "mask_file": mask_file},
        )


class InferenceCeleryService:
    @staticmethod
    def inference(
        *,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
    ) -> None:
        ...

        # gen = Generator()
        # gen.set_model()
