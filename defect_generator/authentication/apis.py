from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from defect_generator.authentication.services import AuthenticationService
from defect_generator.authentication.serializers import UserSignupInputSerializer


class SignupApi(APIView):

    @extend_schema(request=UserSignupInputSerializer)
    def post(self, request):
        serializer = UserSignupInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthenticationService.user_sign_up(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

