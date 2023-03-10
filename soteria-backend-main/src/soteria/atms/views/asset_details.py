from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.atms.models import Asset, AssetType, Floor
from soteria.atms.serializers.assets import AssetTypeDetailSerializer
from soteria.atms.services.asset import create_asset_qr
from soteria.atms.services.asset_details import deactivate_asset, update_asset_details
from soteria.orgs.models import Location


class AssetDetailGetUpdateDeleteAPI(TenantAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        asset_type = AssetTypeDetailSerializer()
        qr_data = serializers.SerializerMethodField()

        class Meta:
            model = Asset
            fields = (
                "id",
                "name",
                "asset_type",
                "floor",
                "tag",
                "location",
                "location_metadata",
                "image_url",
                "qr_data",
            )

        def get_qr_data(self, obj: Asset):
            return create_asset_qr(obj)

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=200, required=False)
        tag = serializers.CharField(max_length=100, required=False)
        floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all(), required=False)
        asset_type_id = serializers.PrimaryKeyRelatedField(queryset=AssetType.objects.all())
        location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
        image_url = serializers.CharField(required=False)
        location_metadata = serializers.CharField(required=False)

        class Meta:
            model = Asset
            fields = (
                "name",
                "tag",
                "floor",
                "asset_type_id",
                "location_id",
                "image_url",
                "location_metadata",
            )

    UpdateOutputSerializer = OutputSerializer
    lookup_url_kwarg = "asset_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Asset.objects.all()
        qs = qs.filter(id=self.kwargs["asset_id"])
        return qs

    def get(self, request, *args, **kwargs):
        asset = self.get_object()
        resp_data = self.OutputSerializer(asset).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        asset = self.get_object()
        serializer = self.InputSerializer(instance=asset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        asset = update_asset_details(asset, data)
        resp_data = self.UpdateOutputSerializer(asset).data
        return self.success_response(resp_data)

    def delete(self, request, *args, **kwargs):
        asset = self.get_object()
        deactivate_asset(asset)
        return self.success_response(
            data={"message": _("Asset is deactivated successfully")},
            status=status.HTTP_200_OK,
        )
