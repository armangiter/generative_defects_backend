from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 4},
)
def result_create(
    self,
    file_path: str,
    file_name: str,
    result_id: int,
):
    logger.info("Start creating result...")

    from defect_generator.defects.services.result import ResultCeleryService

    ResultCeleryService.result_create(
        file_path=file_path, file_name=file_name, result_id=result_id
    )
