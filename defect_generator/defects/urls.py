from django.urls import include, path

from defect_generator.defects.apis.image import ImageApi, ImageDetailApi
from defect_generator.defects.apis.defect_type import (
    DefectTypeApi,
    DefectTypeDetailApi,
)

app_name = "defects"

defect_type_patterns = [
    path("", DefectTypeApi.as_view(), name="defect-types"),
    path("<int:type_id>/", DefectTypeDetailApi.as_view(), name="defect-types-detail"),
    
]

image_patterns = [
    path("", ImageApi.as_view(), name="images"),
    path("<int:image_id>/", ImageDetailApi.as_view(), name="images-detail"),
]


urlpatterns = [
    path("types/", include((defect_type_patterns, "defect-types"))),
    path("images/", include((image_patterns, "images"))),
]
