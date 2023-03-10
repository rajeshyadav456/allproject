import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

from soteria.api.fields import MobileNumberField
from soteria.api.views import GenericAPIView
from soteria.auth.service.mobile_signin import is_valid_mobile_signin_otp, send_mobile_signin_otp
from soteria.auth.views.signin_base import BaseUserSigninView
from soteria.models import User
from soteria.sms.constants import MAX_OTP_LENGTH, MIN_OTP_LENGTH

logger = logging.getLogger(__name__)


class UserMobileSigninAPI(BaseUserSigninView):

    LOGIN_METHOD = "mobile"

    class InputSerializer(serializers.Serializer):
        mobile = MobileNumberField()
        otp = serializers.CharField(max_length=MAX_OTP_LENGTH, min_length=MIN_OTP_LENGTH)

    serializer_class = InputSerializer
    permission_classes = [AllowAny]

    def authenticate_user(self, request, serializer):
        mobile = serializer.data["mobile"]
        otp = serializer.data["otp"]
        user = User.objects.filter(mobile=mobile).first()
        if not user:
            raise serializers.ValidationError(_("No user registered with this mobile number."))
        if not is_valid_mobile_signin_otp(mobile_number=mobile, otp=otp):
            raise serializers.ValidationError(_("Incorrect or expired OTP"))
        logger.info("OTP is successfully verified.")
        return user


class UserMobileSigninSendOTPAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        mobile = MobileNumberField()

        def validate(self, attrs):
            mobile = attrs["mobile"]
            user = User.objects.filter(mobile=mobile).first()
            if not user:
                raise serializers.ValidationError(_("No user registered with this mobile number."))
            attrs["user"] = user
            return attrs

    serializer_class = InputSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        send_mobile_signin_otp(mobile_number=data["mobile"])
        return self.success_response(
            data={"message": _(_("OTP has been sent to mobile number."))},
            status=status.HTTP_200_OK,
        )
