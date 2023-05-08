import logging
from django.db.models import QuerySet


from defect_generator.defects.models import Image, InferenceImage


logger = logging.getLogger(__name__)


class InferenceImageService:

    @staticmethod
    def inference_image_list(*, filters=None) -> QuerySet[Image]:
        return InferenceImage.objects.select_related("inference").all()

    @staticmethod
    def inference_image_get(*, id: int, filters=None) -> Image:
        return InferenceImage.objects.select_related("inference").get(id=id)

    @staticmethod
    def inference_image_delete(*, image_id: int) -> None:
        InferenceImage.objects.filter(id=image_id).delete()
