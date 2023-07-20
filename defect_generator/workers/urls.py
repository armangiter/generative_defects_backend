from django.urls import include, path

from defect_generator.workers.apis.fine_tune_job import FineTuneJobApi
from defect_generator.workers.apis.generate_job import GenerateJobApi

app_name = "workers"

generate_job_patterns = [
    path("", GenerateJobApi.as_view(), name="generate-jobs"),
]

fine_tune_job_patterns = [
    path("", FineTuneJobApi().as_view(), name="fine-tune-jobs"),
]

urlpatterns = [
    path("generate-jobs/", include((generate_job_patterns, "generate-jobs"))),
    path("fine-tune-jobs/", include((fine_tune_job_patterns, "fine-tune-jobs"))),
]
