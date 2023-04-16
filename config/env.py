import os
import environ
from django.core.exceptions import ImproperlyConfigured

# current_env = os.environ["ENVIRONMENT"]
env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2

# if current_env == "dev":
#     ENVIRONMENT.read_env("../.envs/.env.dev")
# elif current_env == "stage":
#     ENVIRONMENT.read_env("../.envs/.env.stage")
# elif current_env == "prod":
#     ENVIRONMENT.read_env("../.envs/.env.prod")
