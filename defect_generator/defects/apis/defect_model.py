from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.defect_model import DefectModelService
from defect_generator.defects.serializers.defect_model import (
    DefectModelInputSerializer,
    DefectModelOutputSerializer,
    DefectModelDetailOutputSerializer,
)


# [POST, GET] api/defects/models/
class DefectModelApi(APIView):
    @extend_schema(request=DefectModelInputSerializer)
    def post(self, request):
        serializer = DefectModelInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            DefectModelService.defect_model_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=DefectModelOutputSerializer)
    def get(self, request):
        query = DefectModelService.defect_model_list()

        serializer = DefectModelOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/models/{model_id}/
class DefectModelDetailApi(APIView):
    @extend_schema(responses=DefectModelDetailOutputSerializer)
    def get(self, request, model_id):
        defect_type = DefectModelService.defect_model_get(model_id=model_id)

        serializer = DefectModelDetailOutputSerializer(defect_type)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, model_id):
        try:
            DefectModelService.defect_model_delete(model_id=model_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
