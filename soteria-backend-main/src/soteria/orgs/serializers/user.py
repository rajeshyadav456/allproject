from rest_framework import serializers

from soteria.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "mobile",
            "mobile_verified",
            "avatar_url",
            "created_at",
            "updated_at",
        )
