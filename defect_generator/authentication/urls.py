from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from defect_generator.authentication.apis import CurrentUserApi, SignupApi


urlpatterns = [
    path("signup/", SignupApi.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("user/", CurrentUserApi.as_view(), name="user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
