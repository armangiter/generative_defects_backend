from django.urls import include, path
from defect_generator.defects.apis.defect_model import (
    DefectModelApi,
    DefectModelDetailApi,
)
from defect_generator.defects.apis.fine_tune import FineTuneApi

from defect_generator.defects.apis.image import ImageApi, ImageDetailApi
from defect_generator.defects.apis.defect_type import DefectTypeApi, DefectTypeDetailApi
from defect_generator.defects.apis.inference import InferenceApi
from defect_generator.defects.apis.result import (
    Result,
    ResultApi,
    ResultDetailApi,
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

inference_patterns = [
    path("", InferenceApi.as_view(), name="inferences"),
]

fine_tune_patterns = [
    path("", FineTuneApi.as_view(), name="fine_tune"),
]

result_patterns = [
    path("", ResultApi.as_view(), name="result"),
    path("<int:result_id>/", ResultDetailApi.as_view(), name="result-detail"),
]

urlpatterns = [
    path("types/", include((defect_type_patterns, "defect-types"))),
    path("images/", include((image_patterns, "images"))),
    path("models/", include((defect_model_patterns, "models"))),
    path("inference/", include((inference_patterns, "inferences"))),
    path("fine_tune/", include((fine_tune_patterns, "fine_tunes"))),
    path("results/", include((result_patterns, "results"))),
]
