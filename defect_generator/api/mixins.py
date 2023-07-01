from functools import wraps
from typing import Sequence, Type
from django.http import HttpResponse

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication



class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

def login_required(f):
    @wraps(f)
    def g(request, *args, **kwargs):
        if request.request.user.is_authenticated:
            return f(request, *args, **kwargs)
        else:
            return HttpResponse('Unauthorized', status=401)
    return g

