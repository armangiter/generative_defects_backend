from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from defect_generator.workers.serializers.generate_job import GenerateJobOutputSerializer
from defect_generator.workers.services.generate_job import GenerateJobService


# [POST, GET] api/defects/types/
class GenerateJobApi(APIView):
    @extend_schema(responses=GenerateJobOutputSerializer)
    def get(self, request):
        
        generating_result = GenerateJobService.get_earliest_generate_job()

        serializer = GenerateJobOutputSerializer(generating_result)

        return Response(serializer.data, status=status.HTTP_200_OK)