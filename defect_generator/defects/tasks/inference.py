from celery import shared_task
from celery.utils.log import get_task_logger

from defect_generator.defects.models import Image

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 4},
)
def inference(
    self,
    defect_type_id: int,
    defect_model_id: int,
    mask_mode: str,
    number_of_images: int,
):
    logger.info("Start inferencing image...")

    from defect_generator.defects.services.inference import InferenceCeleryService

    InferenceCeleryService.inference(
        defect_type_id=defect_type_id,
        defect_model_id=defect_model_id,
        mask_mode=mask_mode,
        number_of_images=number_of_images,
    )
