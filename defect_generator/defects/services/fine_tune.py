import logging, os
from pathlib import Path

from django.db import transaction
from django.core.cache import cache

from defect_generator.defects.models import DefectModel, Image


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

    
    @transaction.atomic
    @staticmethod
    def fine_tune() -> bool:
        lock = cache.get("fine-tune-lock")
        if lock:
            return False
        logger.info("tunning the images ...")
        cache.set("fine-tune-lock", True)
        Image.objects.filter(tuned=False).update(tuned=True)

        return True 
