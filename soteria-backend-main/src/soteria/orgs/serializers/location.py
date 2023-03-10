from rest_framework import serializers

from soteria.orgs.models import Location


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "address",
            "status",
            "city",
            "organization",
        )


class LocationReportSerializer(serializers.ModelSerializer):
    organiztion_name = serializers.CharField(source='organiztion.name')

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "address",
            "status",
            "city",
            "organization",
        )
