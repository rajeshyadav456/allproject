import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

from soteria.api.fields import EmailSerializerField, PasswordSerializersField
from soteria.api.views import GenericAPIView
from soteria.models import ResetPasswordTicket, User

logger = logging.getLogger(__name__)


class ResetPasswordAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = EmailSerializerField()
        password = PasswordSerializersField()
        token = serializers.CharField(max_length=100)

        def validate(self, attrs):
            attrs = super().validate(attrs)
            email = attrs["email"]
            token = attrs["token"]
            user: User = User.objects.filter(email=email).first()
            if user is None:
                raise serializers.ValidationError(_("No user registered with this email"))
            user_ticket: ResetPasswordTicket = ResetPasswordTicket.objects.filter(
                user=user, token=token
            ).first()
            if user_ticket is None or not user_ticket.is_valid_token(user, token):
                raise serializers.ValidationError(_("Invalid or expired ticket"))
            attrs["user"] = user
            attrs["user_ticket"] = user_ticket
            return attrs

    permission_classes = [
        AllowAny,
    ]
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        user: User = data["user"]
        user_ticket: ResetPasswordTicket = data["user_ticket"]
        user.reset_password(raw_password=data["password"])
        user_ticket.reset_token()
        logger.info(f"Password is Successfully reset for user: {user.email}")
        return self.success_response(
            data={
                "message": _("Your password has been reset successfully"),
            },
            status=status.HTTP_200_OK,
        )
