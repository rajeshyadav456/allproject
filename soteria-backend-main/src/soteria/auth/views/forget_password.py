import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

from soteria.api.fields import EmailSerializerField
from soteria.api.views import GenericAPIView
from soteria.auth.service.forget_password import create_and_send_reset_password_ticket
from soteria.models import User

logger = logging.getLogger(__name__)


class ForgotPasswordAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = EmailSerializerField()

    serializer_class = InputSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        user: User = User.objects.filter(email=data["email"]).first()
        if user is None:
            raise serializers.ValidationError(_("No user registered with this email"))
        create_and_send_reset_password_ticket(user, request)
        logger.info(f"Reset password email sent to {user.email}")
        return self.success_response(
            data={"message": _("We sent you a mail to reset your password")},
            status=status.HTTP_200_OK,
        )
