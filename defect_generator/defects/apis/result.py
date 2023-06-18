from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema
from defect_generator.api.utils import inline_serializer

from defect_generator.defects.models import Result, ResultImage
from defect_generator.defects.services.result import ResultService
from defect_generator.defects.utils import get_real_url


# [GET, POST] api/defects/results/
class ResultApi(APIView):
    class ResultInputSerializer(serializers.Serializer):
        image = serializers.FileField()
        defect_type_id = serializers.IntegerField()
        defect_model_id = serializers.IntegerField()

    class ResultOutputSerializer(serializers.ModelSerializer):
        class ResultImageSerializer(serializers.ModelSerializer):
            file = serializers.SerializerMethodField()

            class Meta:
                model = ResultImage
                fields = ["id", "file"]

            def get_file(self, obj: ResultImage):
                if bool(obj.file) is True:
                    return get_real_url(obj.file.url)
                return None

        result_images = ResultImageSerializer(many=True)
        defect_type = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            }
        )
        image = serializers.SerializerMethodField()

        class Meta:
            model = Result
            fields = (
                "id",
                "image",
                "defect_type",
                "defect_model_id",
                "result_images",
                "created",
            )

        def get_image(self, obj: Result):
            if bool(obj.image) is True:
                return get_real_url(obj.image.url)
            return None

    @extend_schema(request=ResultInputSerializer)
    def post(self, request):
        serializer = self.ResultInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = ResultService.result_create(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.ResultOutputSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=ResultOutputSerializer)
    def get(self, request):
        query = ResultService.result_list()

        serializer = self.ResultOutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# [GET, DELETE] api/defects/results/{result_id}/
class ResultDetailApi(APIView):
    class ResultDetailOutputSerializer(serializers.ModelSerializer):
        class ResultImageSerializer2(serializers.ModelSerializer):
            file = serializers.SerializerMethodField()

            class Meta:
                model = ResultImage
                fields = ["id", "file"]

            def get_file(self, obj: ResultImage):
                return get_real_url(obj.file.url)

        result_images = ResultImageSerializer2(many=True)

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

    @extend_schema(responses=ResultDetailOutputSerializer)
    def get(self, request, result_id):
        image = ResultService.result_get(id=result_id)

        serializer = self.ResultDetailOutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, result_id):
        try:
            ResultService.result_delete(image_id=result_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
