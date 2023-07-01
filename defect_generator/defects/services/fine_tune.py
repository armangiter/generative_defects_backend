import logging, os
from pathlib import Path

from django.db import transaction
from django.db.models import QuerySet
from django.core.cache import cache
import requests

from defect_generator.defects.models import DefectModel, DefectType, Image


logger = logging.getLogger(__name__)


class FineTuneService:
    @staticmethod
    def get_fine_tune_status() -> str:
        response = "training" if cache.get("fine-tune-lock") else "ready"
        return response

    @staticmethod
    def finish_fine_tune() -> str:
        # release the lock
        cache.set("fine-tune-lock", False)

    @staticmethod
    @transaction.atomic
    def fine_tune() -> bool:
        lock = cache.get("fine-tune-lock")
        if lock:
            return False
        logger.info("tunning the images ...")
        cache.set("fine-tune-lock", True)

        # create instance prompt
        not_tuned_images = Image.objects.filter(tuned=False)
        images_defect_ids = not_tuned_images.distinct().values_list(
            "defect_type_id", flat=True
        )
        defect_types: list = list(
            DefectType.objects.filter(id__in=images_defect_ids).values_list(
                "command", flat=True
            )
        )
        instance_prompt: str = ",".join(defect_types)
        
        requests.post(
            "http://train_web:8000/train/",
            data={
                "instance_prompt": instance_prompt,
            },
            # files={"image_file": image_file, "mask_file": mask_image_file},
        )
        Image.objects.filter(tuned=False).update(tuned=True)

        return True
