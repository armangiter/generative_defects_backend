from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.weight import WeightService
from defect_generator.defects.serializers.weight import (
    WeightInputSerializer,
    WeightOutputSerializer,
    WeightDetailOutputSerializer,
)


# [POST, GET] api/defects/models/
class WeightApi(APIView):
    @extend_schema(request=WeightInputSerializer)
    def post(self, request):
        serializer = WeightInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            WeightService.weight_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=WeightOutputSerializer)
    def get(self, request):
        query = WeightService.weight_list()

        serializer = WeightOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/models/{model_id}/
class WeightDetailApi(APIView):
    @extend_schema(responses=WeightDetailOutputSerializer)
    def get(self, request, model_id):
        defect_type = WeightService.weight_get(model_id=model_id)

        serializer = WeightDetailOutputSerializer(defect_type)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, model_id):
        try:
            WeightService.weight_delete(model_id=model_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
