from django.urls import include, path

from defect_generator.defects.apis.defect_type import DefectTypeApi, DefectTypeDetailApi
from defect_generator.workers.apis.generate_job import GenerateJobApi

app_name = "workers"

generate_job_patterns = [
    path("", GenerateJobApi.as_view(), name="generate-jobs"),
]

urlpatterns = [
    path("generate-jobs/", include((generate_job_patterns, "generate-jobs"))),
]
