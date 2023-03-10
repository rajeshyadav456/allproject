from rest_framework import serializers

from soteria.atms.models import Asset, AssetType
from soteria.orgs.serializers.location import LocationDetailSerializer


class AssetTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = (
            "id",
            "name",
            "description",
        )


class AssetDetailSerializer(serializers.ModelSerializer):
    asset_type = AssetTypeDetailSerializer()
    location = LocationDetailSerializer()

    class Meta:
        model = Asset
        fields = (
            "id",
            "name",
            "asset_type",
            "location",
            "tag",
        )


class AssetReportSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', allow_null=True, required=False)
    location_address = serializers.CharField(source='location.address', allow_null=True, required=False)
    asset_description = serializers.CharField(source="asset_type.description", allow_null=True, required=False)
    asset_name = serializers.CharField(source="name")

    class Meta:
        model = Asset
        fields = (
            "asset_name",
            "location_name",
            "location_address",
            "tag",
            "asset_description"
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {**representation}
