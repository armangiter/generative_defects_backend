import copy
import logging
import os
from pathlib import Path
import uuid
from zipfile import ZipFile

from django.core.files import File
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache

import requests

from defect_generator.common.services import model_update
from defect_generator.defects.exceptions import AlreadyGeneratingError

from defect_generator.defects.models import DefectModel, DefectType, Result, ResultImage
from defect_generator.defects.serializers.generate import GenerateInputSerializer
from defect_generator.defects.tasks.generate import generate as generate_task
from defect_generator.defects.utils import (
    get_file_extension,
    get_real_url,
    write_file_to_disk,
)
from defect_generator.integrations.aws.client import s3_get_client, s3_get_credentials


logger = logging.getLogger(__name__)
User = get_user_model()


class GenerateService:
    @staticmethod
    def get_generate_status() -> str:
        response = "generating" if cache.get("generate-lock") else "ready"
        return response

    @staticmethod
    def finish_generate(*, result_id: int, user_id: int) -> str:
        # update status of generating result
        print(f"updating result status of result {result_id}")
        result = Result.objects.get(id=result_id)
        result, has_updated = model_update(
            instance=result, fields=["status"], data={"status": Result.STATUS_FINISHED}
        )

        pending_result_exists = Result.objects.filter(
            status=Result.STATUS_PENDING
        ).exists()
        if not pending_result_exists:
            raise AlreadyGeneratingError(
                {"message": "there is no pending generate task."}
            )

        with transaction.atomic():
            result = (
                Result.objects.filter(status=Result.STATUS_PENDING)
                .order_by("created")
                .first()
            )
            print(f"there is a pending generate with result {result.id}")

            print(f"calling the generate service again for result {result.id}")
            user = User.objects.get(id=user_id)
            data = {
                "image_file": result.image,
                "mask_file": result.mask,
                "defect_type_id": result.defect_type_id,
                "defect_model_id": result.defect_model_id,
                "number_of_images": result.number_of_images,
                "mask_mode": result.mask_mode,
            }
            serializer = GenerateInputSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            print(result.id)
            data = serializer.validated_data
            # generate the pending generate task
            GenerateService.generate(
                user=user,
                result_id=result.id,
                image_file=data["image_file"],
                mask_file=data["mask_file"],
                defect_type_id=data["defect_type_id"],
                defect_model_id=data["defect_model_id"],
                mask_mode=data["mask_mode"],
                number_of_images=data["number_of_images"],
            )

    @staticmethod
    def generate(
        *,
        user,
        result_id: int = None,
        image_file: File,
        mask_file: File,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
    ) -> None:
        generating_result_exists = Result.objects.filter(
            status=Result.STATUS_GENERATING
        ).exists()
        if generating_result_exists:
            # put it on the queue to wait for generating task to be finished
            Result.objects.create(
                defect_model_id=defect_model_id,
                defect_type_id=defect_type_id,
                user_id=user.id,
                image=image_file,
                mask=mask_file,
                number_of_images=number_of_images,
                mask_mode=mask_mode,
                status=Result.STATUS_PENDING,
            )
            raise AlreadyGeneratingError(
                {"message": "there is a generate task running already."}
            )

        with transaction.atomic():
            # if this service called from generate_finish service
            if result_id is not None:
                result = Result.objects.get(id=result_id)
                target_image_file = result.image.file
                target_mask_file = result.mask.file
            # if this service called for the first time
            else:
                target_image_file = copy.deepcopy(image_file)
                target_mask_file = copy.deepcopy(mask_file)
                # create a Result with pending status
                result = Result.objects.create(
                    defect_model_id=defect_model_id,
                    defect_type_id=defect_type_id,
                    user_id=user.id,
                    image=image_file,
                    mask=mask_file,
                    number_of_images=number_of_images,
                    mask_mode=mask_mode,
                    status=Result.STATUS_PENDING,
                )

            file_path = write_file_to_disk(file=target_image_file)
            mask_file_path = write_file_to_disk(file=target_mask_file)

            generate_task.delay(
                file_path,
                mask_file_path,
                defect_type_id,
                defect_model_id,
                mask_mode,
                number_of_images,
                result.id,
                user.id,
            )

    @staticmethod
    def finish_generate_new(*, result_id: int, user_id: int) -> str:
        # update status of generating result
        print(f"updating result status of result {result_id}")
        result = Result.objects.get(id=result_id)
        result, has_updated = model_update(
            instance=result, fields=["status"], data={"status": Result.STATUS_FINISHED}
        )

        # get generated images of result
        result_images = ResultImage.objects.filter(result_id=result.id)

        # create a zip file
        zip_file_path = f"zip_file_{result.id}.zip"
        with ZipFile(zip_file_path, "w") as zip_file:
            credentials = s3_get_credentials()
            s3 = s3_get_client(credentials=credentials)

            for image in result_images:
                saved_path = f"{os.path.basename(image.file.name)}"
                s3.download_file(
                    Bucket=credentials.bucket_name,
                    Filename=saved_path,
                    Key=f"media/{image.file.name}",
                )
                zip_file.write(saved_path)
                os.remove(saved_path)

        # uploading zip file
        file_path_object = Path(zip_file_path)
        with file_path_object.open(mode="rb") as file:

            ext = get_file_extension(file_path_object.name)
            file_name = f"{str(uuid.uuid4())}.{ext}"
            
            zip_file = File(file, name=file_name)
            result.zip_file = zip_file
            result.save(update_fields=["zip_file"])

        os.remove(zip_file_path)

    @staticmethod
    def generate_new(
        *,
        user,
        result_id: int = None,
        image_file: File,
        mask_file: File,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
    ) -> None:
        Result.objects.create(
            defect_model_id=defect_model_id,
            defect_type_id=defect_type_id,
            user_id=user.id,
            image=image_file,
            mask=mask_file,
            number_of_images=number_of_images,
            mask_mode=mask_mode,
            status=Result.STATUS_PENDING,
        )


class GenerateCeleryService:
    @staticmethod
    @transaction.atomic
    def generate(
        *,
        file_path: str,
        mask_file_path: str,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int,
        result_id: int,
        user_id: int,
    ) -> None:
        storage = FileSystemStorage()
        file_path_object = Path(file_path)
        mask_path_object = Path(mask_file_path)

        with file_path_object.open(mode="rb") as file, mask_path_object.open(
            mode="rb"
        ) as mask_file:
            logger.info(f"Uploading file: {file.name} ....")

            image_file = File(file, name=file.name)
            mask_image_file = File(mask_file, name=mask_file.name)

            defect_model = DefectModel.objects.get(id=defect_model_id)
            defect_type = (
                DefectType.objects.filter(id=defect_type_id).only("command").get()
            )

            # set the result status "generating"
            result = Result.objects.get(id=result_id)
            model_update(
                instance=result,
                fields=["status"],
                data={"status": Result.STATUS_GENERATING},
            )

            requests.post(
                "http://inference_web:8000/inference/",
                data={
                    "model_url": defect_model.file.url,
                    "number_of_images": number_of_images,
                    "defect_type_id": defect_type_id,
                    "defect_model_id": defect_model_id,
                    "instance_prompt": defect_type.command,
                    "result_id": result_id,
                    "user_id": user_id,
                },
                files={"image_file": image_file, "mask_file": mask_image_file},
            )

            storage.delete(image_file.name)
            storage.delete(mask_image_file.name)
