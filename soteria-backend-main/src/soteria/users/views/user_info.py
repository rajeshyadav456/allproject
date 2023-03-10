import logging

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from soteria.api.fields import EmailSerializerField, MobileNumberField
from soteria.api.views import APIView
from soteria.models import User
from soteria.users.services.user_info import update_user_details

logger = logging.getLogger(__name__)


class UserInfoAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                "id",
                "first_name",
                "last_name",
                "email",
                "mobile",
                "email_verified",
                "mobile_verified",
                "avatar_url",
                "created_at",
                "updated_at",
            )

    class UpdateSerializer(serializers.ModelSerializer):
        email = EmailSerializerField(required=False)
        mobile = MobileNumberField(required=False)
        avatar_url = serializers.CharField(required=False)

        class Meta:
            model = User
            fields = [
                "first_name",
                "last_name",
                "email",
                "mobile",
                "avatar_url",
            ]

    permission_classes = (IsAuthenticated,)
    UpdatedOutputSerializer = OutputSerializer

    def get(self, request, *args, **kwargs):
        resp_data = self.OutputSerializer(request.user).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        serializer = self.UpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        user = update_user_details(user=request.user, data=data)
        logger.info(f"User details updated successfully for user: {user.id}")
        resp_data = self.UpdatedOutputSerializer(user).data
        return self.success_response(resp_data)
