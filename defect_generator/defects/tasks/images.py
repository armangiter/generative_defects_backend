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
def upload_image(
    self,
    file_path: str,
    file_name: str,
    mask_file_path: str,
    mask_file_name: str,
    defect_type_id: int,
):
    logger.info("Start uploading image...")

    from defect_generator.defects.services.image import ImageUploadService

    ImageUploadService.upload_image(
        file_path=file_path,
        file_name=file_name,
        mask_file_path=mask_file_path,
        mask_file_name=mask_file_name,
        defect_type_id=defect_type_id,
    )
