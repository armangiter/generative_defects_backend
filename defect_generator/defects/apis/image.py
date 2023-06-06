from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.models import Image
from defect_generator.defects.services.image import ImageService
from defect_generator.defects.utils import get_real_url


# [POST, GET] api/defects/images/
class ImageApi(APIView):
    class InputSerializer(serializers.Serializer):
        file = serializers.FileField()
        mask_file = serializers.FileField()
        defect_type_id = serializers.IntegerField()

    class OutputSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()
        mask_file = serializers.SerializerMethodField()

        class Meta:
            model = Image
            fields = ("id", "file", "mask_file", "defect_type")

        def get_file(self, obj: Image):
            if bool(obj.file) is True:
                return get_real_url(obj.file.url)
            return None
        
        def get_mask_file(self, obj: Image):
            if bool(obj.mask_file) is True:
                return get_real_url(obj.mask_file.url)
            return None

    @extend_schema(request=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ImageService.image_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = ImageService.image_list()

        serializer = self.OutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/images/{image_id}/
class ImageDetailApi(APIView):
    class InputSerializer(serializers.Serializer):
        file = serializers.FileField()
        mask_file = serializers.FileField()
        defect_type_id = serializers.IntegerField()

    class OutputSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()
        mask_file = serializers.SerializerMethodField()

        class Meta:
            model = Image
            fields = ("id", "file", "mask_file", "defect_type")

        def get_file(self, obj: Image):
            if bool(obj.file) is True:
                return get_real_url(obj.file.url)
            return None
        
        def get_mask_file(self, obj: Image):
            if bool(obj.mask_file) is True:
                return get_real_url(obj.mask_file.url)
            return None

    @extend_schema(responses=OutputSerializer)
    def get(self, request, image_id):
        image = ImageService.image_get(id=image_id)

        serializer = self.OutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(request=InputSerializer)
    def put(self, request, image_id):
        serializer = self.InputSerializer(data=request.data)
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
