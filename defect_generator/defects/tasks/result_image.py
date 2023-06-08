from celery import shared_task
from celery.utils.log import get_task_logger

from defect_generator.defects.models import Image

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
)
def result_image_create(
    self,
    files_path: list[str],
    files_name: list[str],
    result_id: int,
):
    logger.info("Start uploading result image...")

    from defect_generator.defects.services.result_image import ResultImageCeleryService

    print(files_path)
    print(files_name)

    ResultImageCeleryService.image_create(
        files_path=files_path,
        files_name=files_name,
        result_id=result_id,
    )