from functools import lru_cache

import boto3
from attrs import define

from config.utils import assert_settings


@define
class S3Credentials:
    access_key_id: str
    secret_access_key: str
    bucket_name: str
    max_size: int
    endpoint_url: str


@lru_cache
def s3_get_credentials() -> S3Credentials:
    required_config = assert_settings(
        [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_STORAGE_BUCKET_NAME",
            "AWS_S3_ENDPOINT_URL",
            "FILE_MAX_SIZE",
        ],
        "S3 credentials not found.",
    )

    return S3Credentials(
        access_key_id=required_config["AWS_ACCESS_KEY_ID"],
        secret_access_key=required_config["AWS_SECRET_ACCESS_KEY"],
        bucket_name=required_config["AWS_STORAGE_BUCKET_NAME"],
        max_size=required_config["FILE_MAX_SIZE"],
        endpoint_url=required_config["AWS_S3_ENDPOINT_URL"],
    )


def s3_get_client(credentials: S3Credentials = None) -> boto3.client:
    if credentials is None:
        credentials = s3_get_credentials()

    return boto3.client(
        service_name="s3",
        endpoint_url=credentials.endpoint_url,
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )
