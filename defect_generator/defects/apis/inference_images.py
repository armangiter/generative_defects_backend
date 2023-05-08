from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.models import InferenceImage
from defect_generator.defects.services.inference_image import InferenceImageService
from defect_generator.defects.utils import get_real_url


# [GET] api/defects/results/
class InferenceImageApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()
        image = serializers.SerializerMethodField()
        mask_image = serializers.SerializerMethodField()
        defect_type_id = serializers.SerializerMethodField()
        defect_model_id = serializers.SerializerMethodField()

        class Meta:
            model = InferenceImage
            fields = (
                "id",
                "file",
                "image",
                "mask_image",
                "defect_type_id",
                "defect_model_id",
                "created",
            )
            
        def get_file(self, obj: InferenceImage):
            return get_real_url(obj.file.url)
        
        def get_image(self, obj: InferenceImage):
            return obj.inference.image_id

        def get_mask_image(self, obj: InferenceImage):
            return obj.inference.mask_image_id

        def get_defect_type_id(self, obj: InferenceImage):
            return obj.inference.defect_type_id

        def get_defect_model_id(self, obj: InferenceImage):
            return obj.inference.defect_model_id

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = InferenceImageService.inference_image_list()

        serializer = self.OutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/results/{result_id}/
class InferenceImageDetailApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        image = serializers.SerializerMethodField()
        mask_image = serializers.SerializerMethodField()
        defect_type_id = serializers.SerializerMethodField()
        defect_model_id = serializers.SerializerMethodField()

        class Meta:
            model = InferenceImage
            fields = (
                "id",
                "file",
                "image",
                "mask_image",
                "defect_type_id",
                "defect_model_id",
                "created",
            )

        def get_image(self, obj: InferenceImage):
            return obj.inference.image_id

        def get_mask_image(self, obj: InferenceImage):
            return obj.inference.mask_image_id

        def get_defect_type_id(self, obj: InferenceImage):
            return obj.inference.defect_type_id

        def get_defect_model_id(self, obj: InferenceImage):
            return obj.inference.defect_model_id

    @extend_schema(responses=OutputSerializer)
    def get(self, request, result_id):
        image = InferenceImageService.inference_image_get(id=result_id)

        serializer = self.OutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, result_id):
        try:
            InferenceImageService.inference_image_delete(image_id=result_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
