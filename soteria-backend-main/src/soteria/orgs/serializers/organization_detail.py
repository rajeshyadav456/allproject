from rest_framework import serializers

from soteria.models import Organization


class OrganizationDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "status",
            "address",
            "updated_at",
            "created_at",
        )
