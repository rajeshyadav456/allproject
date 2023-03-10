from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from soteria.api.fields import EmailSerializerField, PasswordSerializersField
from soteria.auth.views.signin_base import BaseUserSigninView
from soteria.exception import InvalidCredentials


class UserEmailSigninAPI(BaseUserSigninView):
    LOGIN_METHOD = "email"

    class InputSerializer(serializers.Serializer):
        email = EmailSerializerField()
        password = PasswordSerializersField()

    serializer_class = InputSerializer
    permission_classes = [AllowAny]

    def authenticate_user(self, request, serializer):
        email = serializer.data["email"]
        raw_password = serializer.data["password"]
        user = authenticate(request, **{"username": email, "password": raw_password})
        if user is None:
            raise InvalidCredentials(_("Invalid email or password"))

        return user
