from celery import shared_task


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
)
def generate(
    self,
    image_file_path: str,
    mask_file_path: str,
    defect_type_id: int,
    defect_model_id: int,
    mask_mode: str,
    number_of_images: int,
    result_id: int,
    user_id: int,
):
    from defect_generator.defects.services.generate import GenerateCeleryService

    GenerateCeleryService.generate(
        file_path=image_file_path,
        mask_file_path=mask_file_path,
        defect_type_id=defect_type_id,
        defect_model_id=defect_model_id,
        mask_mode=mask_mode,
        number_of_images=number_of_images,
        result_id=result_id,
        user_id=user_id,
    )
