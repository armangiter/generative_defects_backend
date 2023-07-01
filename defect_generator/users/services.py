from django.db import transaction
from django.db.models.query import QuerySet


from defect_generator.users.filters import UserFilter
from defect_generator.users.models import User
from defect_generator.common.services import model_update
from defect_generator.users.models import User


class UserService:

    @staticmethod
    def user_get(*, id: int, filters=None) -> User:
        return User.objects.get(id=id)
    
    @staticmethod
    def user_create(
        *,
        email: str,
        is_active: bool = True,
        is_admin: bool = False,
        password: str | None = None
    ) -> User:
        user = User.objects.create_user(
            email=email, is_active=is_active, is_admin=is_admin, password=password
        )

        return user

    @transaction.atomic
    @staticmethod
    def user_update(*, user: User, data) -> User:
        non_side_effect_fields = ["first_name", "last_name"]

        user, has_updated = model_update(
            instance=user, fields=non_side_effect_fields, data=data
        )


        # ... some additional tasks with the user ...

        return user


    @staticmethod
    def user_get_login_data(*, user: User):
        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "is_superuser": user.is_superuser,
        }


    @staticmethod
    def user_list(*, filters=None) -> QuerySet[User]:
        filters = filters or {}

        qs = User.objects.all()

        return UserFilter(filters, qs).qs
