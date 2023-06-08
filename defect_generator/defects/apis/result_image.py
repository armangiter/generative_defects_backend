from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.models import Image, ResultImage
from defect_generator.defects.services.image import ImageService
from defect_generator.defects.services.result_image import ResultImageService
from defect_generator.defects.utils import get_real_url


# [POST, GET] api/defects/result-images/
class ResultImageApi(APIView):
    class ResultImageInputSerializer(serializers.Serializer):
        file = serializers.ListField(
            child=serializers.FileField(
                max_length=500, allow_empty_file=False, use_url=False
            )
        )
        result_id = serializers.IntegerField()

    class ResultImageOutputSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()

        class Meta:
            model = ResultImage
            fields = ("id", "result_id", "file")

        def get_file(self, obj: Image):
            if bool(obj.file) is True:
                return get_real_url(obj.file.url)
            return None

    @extend_schema(request=ResultImageInputSerializer(many=True))
    def post(self, request):
        serializer = self.ResultImageInputSerializer(data=request.data)
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

        serializer = self.ResultImageOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/images/{image_id}/
class ResultImageDetailApi(APIView):
    class ResultImageDetailInputSerializer(serializers.Serializer):
        file = serializers.FileField()
        result_id = serializers.IntegerField()

    class ResultImageDetailOutputSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()

        class Meta:
            model = ResultImage
            fields = ("id", "result_id", "file")

        def get_file(self, obj: Image):
            if bool(obj.file) is True:
                return get_real_url(obj.file.url)
            return None

    @extend_schema(responses=ResultImageDetailOutputSerializer)
    def get(self, request, image_id):
        image = ImageService.image_get(id=image_id)

        serializer = self.ResultImageDetailOutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ResultImageDetailInputSerializer)
    def put(self, request, image_id):
        serializer = self.ResultImageDetailInputSerializer(data=request.data)
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
