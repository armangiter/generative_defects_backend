from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.services.fine_tune import FineTuneService


# [POST] api/fine-tune
class FineTuneApi(APIView):

    def post(self, request):
        response = FineTuneService.fine_tune()
        if not response:
            return Response(
                {"status": "already training"}, status=status.HTTP_202_ACCEPTED
            )
        return Response({"status": "train started"}, status=status.HTTP_202_OK)
    

# [GET] api/generate/status
class FineTuneStatusApi(APIView):
    def get(self, request):
        response = FineTuneService.get_fine_tune_status()

        return Response({"status": response}, status=status.HTTP_200_OK)
    
# [POST] api/generate/finish
class FineTuneFinishApi(APIView):
    def post(self, request):
        FineTuneService.finish_fine_tune()

        return Response({"status": "train finished"}, status=status.HTTP_200_OK)