from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

from soteria.api.fields import MobileNumberField
from soteria.api.views import GenericAPIView
from soteria.auth.service.mobile_verify import is_valid_mobile_verify_otp, send_mobile_verify_otp
from soteria.models import User
from soteria.sms.constants import MAX_OTP_LENGTH, MIN_OTP_LENGTH


class MobileVerificationSendOTPAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        mobile = MobileNumberField()

        def validate(self, attrs):
            mobile = attrs["mobile"]
            user = User.objects.filter(mobile=mobile).first()
            if not user:
                raise serializers.ValidationError(
                    _("No user account found with this mobile number")
                )

            attrs["user"] = user
            return attrs

    permission_classes = [AllowAny]
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        mobile = data["mobile"]
        user: User = data["user"]
        send_mobile_verify_otp(user, mobile)

        return self.success_response(
            data={"message": _("OTP has been sent successfully to the mobile number")},
            status=status.HTTP_200_OK,
        )


class MobileVerificationAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        mobile = MobileNumberField()
        otp = serializers.CharField(max_length=MAX_OTP_LENGTH, min_length=MIN_OTP_LENGTH)

        def validate(self, attrs):
            mobile = attrs["mobile"]
            otp = attrs["otp"]
            user = User.objects.filter(mobile=mobile).first()
            if not user:
                raise serializers.ValidationError(
                    _("No user account found with this mobile number")
                )
            if not is_valid_mobile_verify_otp(mobile_number=mobile, otp=otp):
                raise serializers.ValidationError(_("Incorrect or expired OTP"))
            attrs["user"] = user
            return attrs

    permission_classes = [AllowAny]
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        user: User = data["user"]
        user.verify_mobile()
        return self.success_response(
            data={"message": _("Your mobile number is verified and updated successfully")},
            status=status.HTTP_200_OK,
        )


class MobileVerificationReSendOTPAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        mobile = MobileNumberField()

        def validate(self, attrs):
            mobile = attrs["mobile"]
            user = User.objects.filter(mobile=mobile).first()
            if not user:
                raise serializers.ValidationError(
                    _("No user account found with this mobile number")
                )

            attrs["user"] = user
            return attrs

    permission_classes = [AllowAny]
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        mobile = data["mobile"]
        user: User = data["user"]
        send_mobile_verify_otp(user, mobile)

        return self.success_response(
            data={"message": _("OTP has been sent successfully to the mobile number")},
            status=status.HTTP_200_OK,
        )
