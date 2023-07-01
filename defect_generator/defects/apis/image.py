from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.image import ImageService
from defect_generator.defects.serializers.image import (
    ImageInputSerializer,
    ImageOutputSerializer,
    ImageDetailInputSerializer,
    ImageDetailOutputSerializer,
)


# [POST, GET] api/defects/images/
class ImageApi(APIView):
    @extend_schema(request=ImageInputSerializer)
    def post(self, request):
        serializer = ImageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ImageService.image_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=ImageOutputSerializer)
    def get(self, request):
        query = ImageService.image_list()

        serializer = ImageOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/images/{image_id}/
class ImageDetailApi(APIView):
    @extend_schema(responses=ImageDetailOutputSerializer)
    def get(self, request, image_id):
        image = ImageService.image_get(id=image_id)

        serializer = ImageDetailOutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ImageDetailInputSerializer)
    def put(self, request, image_id):
        serializer = ImageDetailInputSerializer(data=request.data)
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
