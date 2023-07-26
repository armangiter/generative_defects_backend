import os
import pathlib, requests, logging
from uuid import uuid4

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from config.env import env

logger = logging.getLogger(__name__)


def file_generate_name(original_file_name):
    extension = pathlib.Path(original_file_name).suffix

    return f"{uuid4().hex}{extension}"


def image_file_generate_upload_path(instance, filename):
    # file_new_name = file_generate_name(original_file_name=filename)
    return f"images/{os.path.basename(filename)}"


def mask_file_generate_upload_path(instance, filename):
    # file_new_name = file_generate_name(original_file_name=filename)
    return f"masks/{os.path.basename(filename)}"


def weights_file_generate_upload_path(instance, filename):
    # file_new_name = file_generate_name(original_file_name=filename)
    return f"weights/{os.path.basename(filename)}"


def results_file_generate_upload_path(instance, filename):
    return f"results/{instance.id}/images/{os.path.basename(filename)}"


def results_mask_file_generate_upload_path(instance, filename):
    return f"results/{instance.id}/masks/{os.path.basename(filename)}"


def result_images_file_generate_upload_path(instance, filename):
    return f"result_images/result_{instance.result_id}/{os.path.basename(filename)}"


def zip_file_generate_upload_path(instance, filename):
    return f"results/{instance.id}/{os.path.basename(filename)}"


def download_file(url: str, file_name: str):
    models_path = os.path.join(settings.MEDIA_ROOT, "models")
    if not os.path.exists(models_path):
        # Create a new directory because it does not exist
        os.makedirs(models_path)

    local_filename = url.split("/")[-1]
    file_name = local_filename.split("?")[0]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192 * 4):
                f.write(chunk)

    save_path = os.path.join(settings.MEDIA_ROOT, "models", file_name)

    # Move to the models folder inside media_root
    os.rename(file_name, save_path)

    print(file_name)
    logger.info(f"Wrote file {file_name} on disk...")
    return save_path


def get_real_url(url: str) -> str:
    real_host: str = f"{env('PUBLIC_MINIO_HOST')}:{env('PUBLIC_MINIO_PORT')}"
    new_url: str = ""
    for part in url.split("/")[3:]:
        new_url += f"{part}/"

    if new_url[-1] == "/":
        new_url = new_url[:-1]

    return f"{real_host}/{new_url}"


def get_file_extension(filename: str):
    return filename.split(".")[-1]


def write_file_to_disk(file: File) -> str:
    storage = FileSystemStorage()
    logger.info(f"file name: {file.name}")
    file.name = storage.get_available_name(file)
    logger.info(f"file name after : {file.name}")
    storage.save(file.name, File(file))
    logger.info(f"Received file: {file.name}")
    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    return file_path
