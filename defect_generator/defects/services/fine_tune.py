import logging, os
from pathlib import Path

from django.db import transaction

from defect_generator.defects.models import DefectModel, Image


logger = logging.getLogger(__name__)


class FineTuneService:
    @transaction.atomic
    @staticmethod
    def fine_tune() -> None:
        logger.info("tunning the images ...")
        Image.objects.filter(tuned=False).update(tuned=True)
