from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.models import Result, ResultImage
from defect_generator.defects.services.result import ResultService
from defect_generator.defects.utils import get_real_url


# [GET] api/defects/results/
class ResultApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class ResultImageSerializer(serializers.ModelSerializer):
            file = serializers.SerializerMethodField()

            class Meta:
                model = ResultImage
                fields = ["id", "file"]
            
            def get_file(self, obj: ResultImage):
                return get_real_url(obj.file.url)

        result_images = ResultImageSerializer(many=True)

        class Meta:
            model = Result
            fields = (
                "id",
                "image",
                # "mask_image",
                "defect_type_id",
                "defect_model_id",
                "result_images",
                "created",
            )

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = ResultService.result_list()

        serializer = self.OutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/results/{result_id}/
class ResultDetailApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class ResultImageSerializer(serializers.ModelSerializer):
            file = serializers.SerializerMethodField()
            
            class Meta:
                model = ResultImage
                fields = ["id", "file"]

            def get_file(self, obj: ResultImage):
                return get_real_url(obj.file.url)
            
        result_images = ResultImageSerializer(many=True)

        class Meta:
            model = Result
            fields = (
                "id",
                "image",
                # "mask_image",
                "defect_type_id",
                "defect_model_id",
                "result_images",
                "created",
            )

    @extend_schema(responses=OutputSerializer)
    def get(self, request, result_id):
        image = ResultService.result_get(id=result_id)

        serializer = self.OutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, result_id):
        try:
            ResultService.result_delete(image_id=result_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
