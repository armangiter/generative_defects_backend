from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.models import DefectType
from defect_generator.defects.services.defect_type import DefectTypeService


# [POST, GET] api/defects/types/
class DefectTypeApi(APIView):
    class DefectTypeInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=127)

    class DefectTypeOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = DefectType
            fields = ("id", "name",)

    @extend_schema(request=DefectTypeInputSerializer)
    def post(self, request):
        serializer = self.DefectTypeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            DefectTypeService.defect_type_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=DefectTypeOutputSerializer)
    def get(self, request):
        query = DefectTypeService.defect_type_list()

        serializer = self.DefectTypeOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, PUT, DELETE] api/defects/types/{type_id}/
class DefectTypeDetailApi(APIView):
    class DefectTypeDetailInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=127)

    class DefectTypeDetailOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = DefectType
            fields = ("id", "name",)

    @extend_schema(responses=DefectTypeDetailOutputSerializer)
    def get(self, request, type_id):
        defect_type = DefectTypeService.defect_type_get(id=type_id)

        serializer = self.DefectTypeDetailOutputSerializer(defect_type)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=DefectTypeDetailInputSerializer, responses=DefectTypeDetailOutputSerializer)
    def put(self, request, type_id):
        serializer = self.DefectTypeDetailInputSerializer(data=request.data)
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
