from django.urls import include, path

# from .apis import DefectTypeApi


urlpatterns = [
    path(
        "defects/",
        include(("defect_generator.defects.urls", "defects"), namespace="defects"),
    ),
    path(
        "users/", include(("defect_generator.users.urls", "users"), namespace="users")
    ),
    path(
        "auth/", include(("defect_generator.authentication.urls", "auth"), namespace="auth")
    ),
]
