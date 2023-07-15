from django.urls import include, path


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
    path(
        "workers/", include(("defect_generator.workers.urls", "workers"), namespace="workers")
    ),
]
