import django_filters

from defect_generator.users.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("id", "email", "is_admin")
