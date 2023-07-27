from celery import shared_task
from celery.utils.log import get_task_logger

from defect_generator.defects.models import DefectType

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
)
def upload_defect_type(
    self,
    file_path: str,
    file_name: str,
    defect_type_id: int,
):
    logger.info("Start uploading defect_type icon_image...")

    from defect_generator.defects.services.defect_type import DefectTypeCeleryService

    DefectTypeCeleryService.defect_type_create(
        file_path=file_path,
        file_name=file_name,
        defect_type_id=defect_type_id,
    )