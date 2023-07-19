from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from defect_generator.workers.serializers.fine_tune_job import FineTuneJobOutputSerializer
from defect_generator.workers.services.fine_tune_job import FineTuneJobService


# [POST, GET] api/defects/types/
class FineTuneJobApi(APIView):
    @extend_schema(responses=FineTuneJobOutputSerializer)
    def get(self, request):
        
        generating_result = FineTuneJobService.get_earliest_fine_tune_job()

        serializer = FineTuneJobOutputSerializer(generating_result)

        return Response(serializer.data, status=status.HTTP_200_OK)