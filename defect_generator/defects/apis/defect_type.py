from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.defect_type import DefectTypeService
from defect_generator.defects.serializers.defect_type import (
    DefectTypeFilterSerializer,
    DefectTypeInputSerializer,
    DefectTypeOutputSerializer,
    DefectTypeDetailInputSerializer,
    DefectTypeDetailOutputSerializer,
)


# [POST, GET] api/defects/types/
class DefectTypeApi(APIView):
    @extend_schema(request=DefectTypeInputSerializer)
    def post(self, request):
        serializer = DefectTypeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            DefectTypeService.defect_type_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[DefectTypeFilterSerializer], responses=DefectTypeOutputSerializer
    )
    def get(self, request):
        filters = None
        if request.query_params:
            filters_serializer = DefectTypeFilterSerializer(
                data=request.query_params
            )
            filters_serializer.is_valid(raise_exception=True)
            filters = filters_serializer.validated_data

        query = DefectTypeService.defect_type_list(filters=filters)

        serializer = DefectTypeOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, PUT, DELETE] api/defects/types/{type_id}/
class DefectTypeDetailApi(APIView):

    @extend_schema(responses=DefectTypeDetailOutputSerializer)
    def get(self, request, type_id):
        defect_type = DefectTypeService.defect_type_get(id=type_id)

        serializer = DefectTypeDetailOutputSerializer(defect_type)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=DefectTypeDetailInputSerializer,
        responses=DefectTypeDetailOutputSerializer,
    )
    def put(self, request, type_id):
        serializer = DefectTypeDetailInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            DefectTypeService.defect_type_update(
                type_id=type_id, **serializer.validated_data
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, type_id):
        try:
            DefectTypeService.defect_type_delete(type_id=type_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
