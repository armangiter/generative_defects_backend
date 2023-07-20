from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema
from defect_generator.api.mixins import ApiAuthMixin
from defect_generator.defects.serializers.fine_tune import (
    FineTuneDetailInputSerializer,
    FineTuneDetailOutputSerializer,
    FineTuneFilterSerializer,
    FineTuneInputSerializer,
    FineTuneOutputSerializer,
)

from defect_generator.defects.services.fine_tune import FineTuneService


# [POST, GET] api/fine-tunes/
class FineTuneApi(ApiAuthMixin, APIView):
    @extend_schema(request=FineTuneInputSerializer)
    def post(self, request):
        FineTuneService.fine_tune_create(user=request.user)

        return Response({"status": "fine tune started"}, status=status.HTTP_202_OK)

    @extend_schema(
        parameters=[FineTuneFilterSerializer], responses=FineTuneOutputSerializer
    )
    def get(self, request):
        filter_serializer = FineTuneFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        query = FineTuneService.fine_tune_list(user=request.user, filters=filters)

        serializer = FineTuneOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, PUT, DELETE] api/fine-tunes/{fine_tune_id}/
class FineTuneDetailApi(ApiAuthMixin, APIView):
    def get_permissions(self):
        # remove IsAuthenticated permission for put method
        if self.request.method == "PUT":
            return []
        else:
            return super().get_permissions()

    @extend_schema(responses=FineTuneDetailOutputSerializer)
    def get(self, request, fine_tune_id):
        fine_tune = FineTuneService.fine_tune_get(fine_tune_id=fine_tune_id)

        serializer = FineTuneDetailOutputSerializer(fine_tune)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=FineTuneDetailInputSerializer)
    def put(self, request, fine_tune_id):
        serializer = FineTuneDetailInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            FineTuneService.fine_tune_update(
                fine_tune_id=fine_tune_id, **serializer.validated_data
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, fine_tune_id):
        try:
            FineTuneService.fine_tune_delete(fine_tune_id=fine_tune_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
