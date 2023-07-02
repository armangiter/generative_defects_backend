from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class AlreadyGeneratingError(APIException):
    status_code = status.HTTP_202_ACCEPTED
    default_detail = _("There is a generate task running already.")
    default_code = "already_generating"
