from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from soteria.api.fields import EmailSerializerField
from soteria.api.views import GenericAPIView
from soteria.auth.service.email_verify import is_valid_email_verify_otp, send_verify_email_otp
from soteria.models import User


class EmailVerificationSendOTPAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = EmailSerializerField()

        def validate(self, attrs):
            email = str(attrs["email"]).lower()
            user = User.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError(_("No user account found with this email"))

            attrs["user"] = user
            return attrs

    permission_classes = [AllowAny]
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)

        send_verify_email_otp(data["user"])

        return self.success_response(
            data={"message": _("We have sent a OTP to your email successfully")}
        )


class EmailVerificationVerifyOTPAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = EmailSerializerField()
        otp = serializers.CharField(max_length=10)

        def validate(self, attrs):
            email = str(attrs["email"]).lower()
            otp = attrs["otp"]
            user = User.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError(_("No user account found with this email"))

            if not is_valid_email_verify_otp(user, otp):
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
        user.verify_email()
        return self.success_response(
            data={"message": _("Your email has been verified successfully.")}
        )


class EmailVerificationReSendOTPAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = EmailSerializerField()

        def validate(self, attrs):
            email = str(attrs["email"]).lower()
            user = User.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError(_("No user account found with this email"))

            attrs["user"] = user
            return attrs

    permission_classes = [AllowAny]
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        send_verify_email_otp(data["user"])
        return self.success_response(
            data={"message": _("We have sent a OTP to your email successfully")}
        )
