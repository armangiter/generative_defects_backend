from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema
from defect_generator.api.mixins import ApiAuthMixin

from defect_generator.api.utils import inline_serializer

from defect_generator.defects.services.result import ResultService
from defect_generator.defects.serializers.result import (
    ResultFilterSerializer,
    ResultInputSerializer,
    ResultOutputSerializer,
    ResultDetailInputSerializer,
    ResultDetailOutputSerializer,
)


# [GET, POST] api/defects/results/
class ResultApi(ApiAuthMixin, APIView):

    @extend_schema(request=ResultInputSerializer)
    def post(self, request):
        serializer = ResultInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = ResultService.result_create(user=request.user, **serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        serializer = ResultOutputSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[ResultFilterSerializer], responses=ResultOutputSerializer
    )
    def get(self, request):
        filter_serializer = ResultFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        query = ResultService.result_list(user=request.user,filters=filters)

        serializer = ResultOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/results/{result_id}/
class ResultDetailApi(ApiAuthMixin, APIView):
    def get_permissions(self):
        # remove IsAuthenticated permission for put method
        if self.request.method == "PUT":
            return []
        else:
            return super().get_permissions()
        
    @extend_schema(request=ResultDetailInputSerializer)
    def put(self, request, result_id):
        serializer = ResultDetailInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ResultService.result_update(result_id=result_id, **serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    @extend_schema(responses=ResultDetailOutputSerializer)
    def get(self, request, result_id):
        image = ResultService.result_get(id=result_id)

        serializer = ResultDetailOutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, result_id):
        try:
            ResultService.result_delete(image_id=result_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
