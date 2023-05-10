import logging
from django.db.models import QuerySet


from defect_generator.defects.models import Image, Result, ResultImage


logger = logging.getLogger(__name__)


class ResultService:
    @staticmethod
    def result_list(*, filters=None) -> QuerySet[Image]:
        return Result.objects.prefetch_related("result_images").all()

    @staticmethod
    def result_get(*, id: int, filters=None) -> Image:
        return Result.objects.prefetch_related("result_images").get(id=id)

    @staticmethod
    def result_delete(*, image_id: int) -> None:
        Result.objects.filter(id=image_id).delete()
