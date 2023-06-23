import os
from pathlib import Path

from config.env import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = "django-insecure-3nff8m$d$ih#^+^+%7yafv2_2u9tvspoiqpdop_1(ccc86&p)-"

DEBUG = True

ALLOWED_HOSTS = [
    "128.65.167.198",
    "127.0.0.1",
    "localhost",
    "generative",
    "153.156.254.150",
]


LOCAL_APPS = [
    "defect_generator.defects.apps.DefectsConfig",
    "defect_generator.integrations.apps.IntegrationsConfig",
    "defect_generator.api.apps.ApiConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "django_extensions",
    "debug_toolbar",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8997",
    "http://localhost:8995",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:9000",
    "http://153.156.254.150:50828",
    "http://localhost:82"
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ],
}

ROOT_URLCONF = "config.urls"

SHELL_PLUS_PRINT_SQL = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT_NAME = "media"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SPECTACULAR_SETTINGS = {
    "TITLE": "Rutilea Defects Generator API",
    "DESCRIPTION": "Defect Generator",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MINIO_ACCESS_KEY = env("MINIO_ROOT_USER")
MINIO_SECRET_KEY = env("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME = env("MINIO_BUCKET_NAME")
MINIO_ENDPOINT = env("MINIO_ENDPOINT")

FILE_MAX_SIZE = env.int("FILE_MAX_SIZE", default=10485760 * 20)  # 100 MiB
FILE_UPLOAD_STORAGE = env("FILE_UPLOAD_STORAGE")

FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB

if FILE_UPLOAD_STORAGE == "LOCAL":
    MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"

if FILE_UPLOAD_STORAGE == "S3":
    DEFAULT_FILE_STORAGE = "config.storage_backends.PublicMediaStorage"

    AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
    AWS_QUERYSTRING_AUTH = False

    _AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default="")

    if _AWS_S3_CUSTOM_DOMAIN:
        AWS_S3_CUSTOM_DOMAIN = _AWS_S3_CUSTOM_DOMAIN


# https://docs.celeryproject.org/en/stable/userguide/configuration.html
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = "UTC"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("CACHE_LOCATION"),
        "TIMEOUT": 604800,  # 7 days
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "api": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "DEBUG"),
        },
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[{asctime}] ({levelname}) - {name} - {message}",
            "datefmt": "%Y/%m/%d %H:%M:%S",
            "style": "{",
        }
    },
}
