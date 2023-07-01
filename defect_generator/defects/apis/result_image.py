from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.image import ImageService
from defect_generator.defects.services.result_image import ResultImageService
from defect_generator.defects.serializers.result_image import (
    ResultImageInputSerializer,
    ResultImageOutputSerializer,
    ResultImageDetailInputSerializer,
    ResultImageDetailOutputSerializer,
)


# [POST, GET] api/defects/result-images/
class ResultImageApi(APIView):
    @extend_schema(request=ResultImageInputSerializer(many=True))
    def post(self, request):
        serializer = ResultImageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ResultImageService.image_create(
                files=serializer.validated_data["file"],
                result_id=serializer.validated_data["result_id"],
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=ResultImageOutputSerializer)
    def get(self, request):
        query = ResultImageService.image_list()

        serializer = ResultImageOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/result-images/{result_image_id}/
class ResultImageDetailApi(APIView):
    @extend_schema(responses=ResultImageDetailOutputSerializer)
    def get(self, request, image_id):
        image = ImageService.image_get(id=image_id)

        serializer = ResultImageDetailOutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ResultImageDetailInputSerializer)
    def put(self, request, image_id):
        serializer = ResultImageDetailInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ImageService.image_update(image_id=image_id, **serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, image_id):
        try:
            ImageService.image_delete(image_id=image_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
