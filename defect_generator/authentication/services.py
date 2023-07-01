from django.db import transaction
from django.contrib.auth import get_user_model


User = get_user_model()


class AuthenticationService:
    @transaction.atomic
    @staticmethod
    def user_sign_up(*, email: str, password: str) -> User:
        return User.objects.create_user(email=email, password=password)
