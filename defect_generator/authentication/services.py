from django.db import transaction
from django.contrib.auth import get_user_model

from defect_generator.authentication.serializers import CurrentUserOutputSerializer


User = get_user_model()


class AuthenticationService:
    @staticmethod
    @transaction.atomic
    def user_sign_up(*, email: str, password: str) -> User:
        return User.objects.create_user(email=email, password=password)
    
    @staticmethod
    def get_logged_in_user(*, user: User):
        serializer = CurrentUserOutputSerializer(user)
        return serializer.data