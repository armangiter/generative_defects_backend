from django.urls import include, path
# from .apis import DefectTypeApi


urlpatterns = [
    path("defects/", include(("defect_generator.defects.urls", "defects"), namespace="defects")),
]


    