from django.db.models import QuerySet

from defect_generator.defects.models import Weight

from django.core.files import File

class WeightService:

    @staticmethod
    def weight_create(*, file: File) -> None:
        Weight.objects.create(file=file)
    
    @staticmethod
    def weight_list(*, filters=None) -> QuerySet[Weight]:
        return Weight.objects.all()
    
    @staticmethod
    def weight_get(*, weight_id: int, filters=None) -> Weight:
        return Weight.objects.get(id=weight_id)

    @staticmethod
    def weight_delete(*, weight_id: int) -> None:
        Weight.objects.filter(id=weight_id).delete(id=weight_id)