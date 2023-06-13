import logging, os
from pathlib import Path

from django.db import transaction
import requests

from defect_generator.defects.models import DefectModel, Image


logger = logging.getLogger(__name__)


class FineTuneService:

    @staticmethod
    def get_fine_tune_status() -> str:
        # response = requests.get("http://inference_web:8000/status").json()
        response = {"status": "ready"}
        return response["status"]
    
    @transaction.atomic
    @staticmethod
    def fine_tune() -> None:
        logger.info("tunning the images ...")
        Image.objects.filter(tuned=False).update(tuned=True)
