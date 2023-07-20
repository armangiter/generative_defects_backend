from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
)
def upload_weight(
    self,
    file_path: str,
    file_name: str,
):
    logger.info("Uploading weight...")

    from defect_generator.defects.services.weight import WeightCeleryService

    WeightCeleryService.weight_create(
        file_path=file_path,
        file_name=file_name,
    )