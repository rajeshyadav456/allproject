from rest_framework import serializers

from soteria import roles
from soteria.orgs.models import OrganizationMember
from soteria.orgs.serializers.organization_detail import OrganizationDetailOutputSerializer
from soteria.orgs.serializers.user import UserSerializer


class OrganizationMemberRoleSerializer(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = roles.get_choices()
        super().__init__(choices, **kwargs)

    def to_representation(self, value):
        return roles.get(value).to_public_info()


class OrganizationMemberDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationDetailOutputSerializer()
    user = UserSerializer()

    class Meta:
        model = OrganizationMember
        fields = (
            "id",
            "email",
            "mobile",
            "token",
            "token_expires_at",
            "role",
            "location",
            "organization",
            "user",
            "updated_at",
            "created_at",
        )
