import logging, os
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from config.env import BASE_DIR

import PIL 

from defect_generator.defects.models import Image, DefectModel, DefectType
from defect_generator.defects.tasks.inference import inference as inference_task
from defect_generator.defects.utils import download_file
from generative_defects.generator import Generator


logger = logging.getLogger(__name__)

class InferenceService:
    @staticmethod
    def inference(
        *,
        image_file: File,
        mask_file: File,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int
    ) -> None:
        defect_model = DefectModel.objects.get(id=defect_model_id)
        
        # Download model
        model_path = download_file(url=defect_model.file.url, file_name=defect_model.file.name)

        # Write files to the disk
        storage = FileSystemStorage()
        logger.info(f"file name: {image_file.name}")
        image_file.name = storage.get_available_name(image_file)
        logger.info(f"file name after : {image_file.name}")
        IMAGES_PATH = os.path.join(settings.MEDIA_ROOT, "images", image_file.name)
        storage.save(IMAGES_PATH, File(image_file))
        logger.info(f"Received file: {image_file.name}")
        image_file_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
        print(image_file.name)
        print(image_file_path)


        storage = FileSystemStorage()
        logger.info(f"file name: {mask_file.name}")
        mask_file.name = storage.get_available_name(mask_file)
        logger.info(f"file name after : {mask_file.name}")
        MASK_IMAGES_PATH = os.path.join(settings.MEDIA_ROOT, "masks", mask_file.name)
        storage.save(MASK_IMAGES_PATH, File(mask_file))
        logger.info(f"Received file: {mask_file.name}")
        mask_file_path = os.path.join(settings.MEDIA_ROOT, mask_file.name)
        print(mask_file.name)
        print(mask_file_path)

        gen = Generator()

        print("Setting model")
        gen.set_model(model_path, 9)

        print("Start generating images")
        image = PIL.Image.open(image_file_path).convert("RGB").resize((512, 512))
        mask_image = PIL.Image.open(mask_file_path).convert("RGB").resize((512, 512))
        save_path="./generate"

        images = gen.generate(image=image, mask=mask_image, input_promt="a sks dog sitting on a bench")

        for idx, img in enumerate(images):
            img.save(os.path.join(save_path,f"results_{idx}.jpg"))
        print("Done generating")


        # gen = Generator()
        # gen.set_model(defect_model.file)

class InferenceCeleryService:
    @staticmethod
    def inference(
        *,
        defect_type_id: int,
        defect_model_id: int,
        mask_mode: str,
        number_of_images: int
    ) -> None:
        ...
        
        # gen = Generator()
        # gen.set_model()

