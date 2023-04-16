from django.db import transaction
from django.db.models import QuerySet

from defect_generator.defects.models import DefectType


class DefectTypeService:

    @staticmethod
    def defect_type_create(*, name: str) -> None:
        DefectType.objects.create(name=name)
    
    @staticmethod
    def defect_type_list(*, filters=None) -> QuerySet[DefectType]:
        return DefectType.objects.all()
    
    @staticmethod
    def defect_type_get(*, id: int, filters=None) -> DefectType:
        return DefectType.objects.get(id=id)
    
    @staticmethod
    def defect_type_update(*, type_id: int, name: str) -> None:
        DefectType.objects.filter(id=type_id).update(name=name)

    @staticmethod
    def defect_type_delete(*, type_id: int) -> None:
        DefectType.objects.filter(id=type_id).delete(id=type_id)