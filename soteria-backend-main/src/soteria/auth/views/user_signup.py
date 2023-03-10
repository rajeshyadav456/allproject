import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

from soteria.api.fields import EmailSerializerField, MobileNumberField, PasswordSerializersField
from soteria.api.views import GenericAPIView
from soteria.auth.service.user_signup import create_user
from soteria.models import InvitationCode

logger = logging.getLogger(__name__)


class UserSignupAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        invitation_code = serializers.CharField(max_length=100)
        first_name = serializers.CharField(max_length=100)
        last_name = serializers.CharField(max_length=100)
        email = EmailSerializerField()
        mobile = MobileNumberField()
        password = PasswordSerializersField()

        def validate(self, attrs):
            invitation_code = InvitationCode.objects.filter(
                user_id=None, is_used=False, code=attrs["invitation_code"]
            ).first()
            if not invitation_code:
                raise serializers.ValidationError("Invalid invitation code")
            return attrs

    serializer_class = InputSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        user = create_user(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            mobile=data["mobile"],
            password=data["password"],
            invitation_code=data["invitation_code"],
        )
        logger.info(f"User is created successfully : {user}")
        return self.success_response(
            data={"message": _("Account successfully created.")},
            status=status.HTTP_201_CREATED,
        )
