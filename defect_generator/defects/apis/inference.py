from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.inference import InferenceService


# [POST] api/inference
class InferenceApi(APIView):

    class InputSerializer(serializers.Serializer):
        image_file = serializers.FileField()
        mask_file = serializers.FileField()
        defect_type_id = serializers.IntegerField()
        defect_model_id = serializers.IntegerField()
        mask_mode = serializers.ChoiceField([("random", "Random"), ("in_paint", "In Paint")])
        number_of_images = serializers.IntegerField()

    @extend_schema(request=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            InferenceService.inference(**serializer.validated_data)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)