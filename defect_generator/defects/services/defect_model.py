from django.db import transaction
from django.db.models import QuerySet

from defect_generator.defects.models import DefectModel, DefectType

from django.core.files import File

class DefectModelService:

    @staticmethod
    def defect_model_create(*, file: File) -> None:
        DefectModel.objects.create(file=file)
    
    @staticmethod
    def defect_model_list(*, filters=None) -> QuerySet[DefectModel]:
        return DefectModel.objects.all()
    