from rest_framework import serializers
from rest_framework import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from defect_generator.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from defect_generator.users.models import User
from defect_generator.users.services import UserService


class UserListApi(APIView):
    class UserPagination(LimitOffsetPagination):
        default_limit = 1

    class UserFilterSerializer(serializers.Serializer):
        is_admin = serializers.BooleanField(
            required=False, allow_null=True, default=None
        )
        email = serializers.EmailField(required=False)

    class UserListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "email", "is_admin")

    @extend_schema(
        responses=UserListOutputSerializer,
        parameters=[UserFilterSerializer],
    )
    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.UserFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = UserService.user_list(filters=filters_serializer.validated_data)

        serializer = self.UserListOutputSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class UserDetailApi(APIView):
    class UserDetailOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "email", "is_admin")

    @extend_schema(
        responses=UserDetailOutputSerializer,
    )
    def get(self, request, user_id):
        try:
            user = UserService.user_get(id=user_id)
        except User.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "user with provided user_id does not exists."}
            )

        serializer = self.UserDetailOutputSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
