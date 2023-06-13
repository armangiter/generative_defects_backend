from django.urls import include, path
from defect_generator.defects.apis.defect_model import (
    DefectModelApi,
    DefectModelDetailApi,
)
from defect_generator.defects.apis.fine_tune import FineTuneApi
from defect_generator.defects.apis.generate import GenerateApi, GenerateStatusApi

from defect_generator.defects.apis.image import ImageApi, ImageDetailApi
from defect_generator.defects.apis.defect_type import DefectTypeApi, DefectTypeDetailApi
from defect_generator.defects.apis.result import (
    Result,
    ResultApi,
    ResultDetailApi,
)
from defect_generator.defects.apis.result_image import (
    ResultImageApi,
    ResultImageDetailApi,
)

app_name = "defects"

defect_type_patterns = [
    path("", DefectTypeApi.as_view(), name="defect-types"),
    path("<int:type_id>/", DefectTypeDetailApi.as_view(), name="defect-types-detail"),
]

defect_model_patterns = [
    path("", DefectModelApi.as_view(), name="defect-models"),
    path(
        "<int:model_id>/", DefectModelDetailApi.as_view(), name="defect-models-detail"
    ),
]

image_patterns = [
    path("", ImageApi.as_view(), name="images"),
    path("<int:image_id>/", ImageDetailApi.as_view(), name="images-detail"),
]

generate_patterns = [
    path("", GenerateApi.as_view(), name="generate"),
    path("status/", GenerateStatusApi.as_view(), name="generate-status"),
]

fine_tune_patterns = [
    path("", FineTuneApi.as_view(), name="fine_tune"),
]

result_patterns = [
    path("", ResultApi.as_view(), name="result"),
    path("<int:result_id>/", ResultDetailApi.as_view(), name="result-detail"),
]

result_images_patterns = [
    path("", ResultImageApi.as_view(), name="result-images"),
    path("<int:result_image_id>/", ResultImageDetailApi.as_view(), name="result-image-detail"),
]

urlpatterns = [
    path("types/", include((defect_type_patterns, "defect-types"))),
    path("images/", include((image_patterns, "images"))),
    path("models/", include((defect_model_patterns, "models"))),
    # path("inference/", include((inference_patterns, "inferences"))),
    path("generate/", include((generate_patterns, "generates"))),
    path("fine_tune/", include((fine_tune_patterns, "fine_tunes"))),
    path("results/", include((result_patterns, "results"))),
    path("result-images/", include((result_images_patterns, "results-images"))),
]
