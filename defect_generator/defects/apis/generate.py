from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from defect_generator.api.mixins import ApiAuthMixin
from defect_generator.defects.exceptions import AlreadyGeneratingError

from defect_generator.defects.services.generate import GenerateService
from defect_generator.defects.serializers.generate import GenerateFinishInputSerializer, GenerateInputSerializer


# [POST] api/generate
class GenerateApi(ApiAuthMixin, APIView):
    @extend_schema(request=GenerateInputSerializer)
    def post(self, request):
        serializer = GenerateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            GenerateService.generate_new(
                user=request.user, **serializer.validated_data
            )
        except AlreadyGeneratingError:
            ...
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"status": "generate started"}, status=status.HTTP_202_ACCEPTED)


# [GET] api/generate/status
class GenerateStatusApi(APIView):
    def get(self, request):
        response = GenerateService.get_generate_status()

        return Response({"status": response}, status=status.HTTP_200_OK)


# [POST] api/generate/finish
class GenerateFinishApi(APIView):
    @extend_schema(request=GenerateFinishInputSerializer)
    def post(self, request):
        serializer = GenerateFinishInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        GenerateService.finish_generate_new(**serializer.validated_data)

        return Response({"status": "generate finished"}, status=status.HTTP_200_OK)
