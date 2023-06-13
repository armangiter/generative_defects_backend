from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.generate import GenerateService


# [POST] api/generate
class GenerateApi(APIView):
    class GenerateInputSerializer(serializers.Serializer):
        image_file = serializers.FileField()
        mask_file = serializers.FileField()
        defect_type_id = serializers.IntegerField()
        defect_model_id = serializers.IntegerField()
        mask_mode = serializers.ChoiceField(
            [("random", "Random"), ("in_paint", "In Paint")]
        )
        number_of_images = serializers.IntegerField()

    @extend_schema(request=GenerateInputSerializer)
    def post(self, request):
        serializer = self.GenerateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = GenerateService.generate(**serializer.validated_data)
        if not response:
            return Response(
                {"status": "already generating"}, status=status.HTTP_202_ACCEPTED
            )
        return Response({"status": "generate started"}, status=status.HTTP_202_ACCEPTED)


# [GET] api/generate/status
class GenerateStatusApi(APIView):
    def get(self, request):
        response = GenerateService.get_generate_status()

        return Response({"status": response}, status=status.HTTP_200_OK)


# [POST] api/generate/finish
class GenerateFinishApi(APIView):
    def post(self, request):
        GenerateService.finish_generate()

        return Response({"status": "generate finished"}, status=status.HTTP_200_OK)
