from django.db.models import QuerySet

from defect_generator.defects.models import DefectModel

from django.core.files import File

class DefectModelService:

    @staticmethod
    def defect_model_create(*, file: File) -> None:
        DefectModel.objects.create(file=file)
    
    @staticmethod
    def defect_model_list(*, filters=None) -> QuerySet[DefectModel]:
        return DefectModel.objects.all()
    
    @staticmethod
    def defect_model_get(*, model_id: int, filters=None) -> DefectModel:
        return DefectModel.objects.get(id=model_id)

    @staticmethod
    def defect_model_delete(*, model_id: int) -> None:
        DefectModel.objects.filter(id=model_id).delete(id=model_id)