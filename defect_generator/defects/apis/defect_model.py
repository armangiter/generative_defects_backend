from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.models import DefectModel, DefectType
from defect_generator.defects.services.defect_model import DefectModelService
from defect_generator.defects.services.inference import InferenceService


# [POST, GET] api/defects/models/
class DefectModelApi(APIView):
    class InputSerializer(serializers.Serializer):
        file = serializers.FileField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = DefectModel
            fields = ("id", "name", "file",)

    @extend_schema(request=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            DefectModelService.defect_model_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = DefectModelService.defect_model_list()

        serializer = self.OutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# [GET, DELETE] api/defects/types/{type_id}/
class DefectModelDetailApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=127)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = DefectType
            fields = ("id", "name", "file")

    @extend_schema(responses=OutputSerializer)
    def get(self, request, model_id):
        defect_type = DefectModelService.defect_model_get(model_id=model_id)

        serializer = self.OutputSerializer(defect_type)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, model_id):
        try:
            DefectModelService.defect_model_delete(model_id=model_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)