import os
import pathlib, requests, logging
from uuid import uuid4

from django.conf import settings

from config.env import env

logger = logging.getLogger(__name__)


def file_generate_name(original_file_name):
    extension = pathlib.Path(original_file_name).suffix

    return f"{uuid4().hex}{extension}"


def image_file_generate_upload_path(instance, filename):
    file_new_name = file_generate_name(original_file_name=filename)
    return f"images/{file_new_name}"


def mask_file_generate_upload_path(instance, filename):
    file_new_name = file_generate_name(original_file_name=filename)
    return f"masks/{file_new_name}"


def defect_models_file_generate_upload_path(instance, filename):
    file_new_name = file_generate_name(original_file_name=filename)
    return f"defect_models/{file_new_name}"


def inference_images_file_generate_upload_path(instance, filename):
    file_new_name = file_generate_name(original_file_name=filename)
    return f"inference_images/{file_new_name}"


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
    real_host: str = f"{env('HOST_URL')}:9000"
    new_url: str = ""
    for part in url.split("/")[3:]:
        new_url += f"{part}/"

    if new_url[-1] == "/":
        new_url = new_url[:-1]

    return f"{real_host}/{new_url}"
    