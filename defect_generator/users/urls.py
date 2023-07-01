from django.urls import path

from .apis import UserDetailApi, UserListApi

urlpatterns = [
    path("", UserListApi.as_view(), name="user-list"),
    path("<int:user_id>/", UserDetailApi.as_view(), name="user-detail"),
]
