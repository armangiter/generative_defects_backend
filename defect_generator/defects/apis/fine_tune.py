from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

# from defect_generator.defects.services.fine_tune import InferenceService


# [POST] api/fine-tune
class FineTuneApi(APIView):

    def post(self, request):
        # Simple dummy response for now
        return Response(status=status.HTTP_200_OK)