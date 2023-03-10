from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from soteria.api.views import GenericAPIView
from soteria.exception import UserEmailUnverified, UserMobileUnverified
from soteria.models import User


class BaseUserSigninView(GenericAPIView):
    """Base class for all types of user signin process."""

    # either 'email' or 'mobile'
    LOGIN_METHOD = None

    def authenticate_user(self, request, serializer) -> User:
        """Super class must implement this method and return authenticated
        user"""
        raise NotImplementedError(".authenticate_user() must be overridden.")

    def login_user(self, request, user) -> RefreshToken:
        if self.LOGIN_METHOD == "email" and user.email and not user.email_verified:
            raise UserEmailUnverified()

        if self.LOGIN_METHOD == "mobile" and user.mobile and not user.mobile_verified:
            raise UserMobileUnverified()

        refresh = RefreshToken.for_user(user)

        # update last login of user
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        return refresh

    def do_login_and_prepare_response(self, request, user):
        # get access and refresh token
        refresh = self.login_user(request, user)

        return self.success_response(
            status=status.HTTP_200_OK,
            data={
                "refresh_token": str(refresh),
                "refresh_exp_at": refresh["exp"],
                "access_token": str(refresh.access_token),
                "access_exp_at": refresh.access_token["exp"],
            },
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.authenticate_user(request, serializer)
        if user is None:
            raise Exception("'authenticate_request' must return user instance")

        return self.do_login_and_prepare_response(request, user)
