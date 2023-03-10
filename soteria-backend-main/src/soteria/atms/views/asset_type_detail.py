from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.atms.models import AssetType
from soteria.atms.services.asset_type import deactivate_asset_type, update_asset_type


class AssetTypeDetailGetUpdateDeleteAPI(TenantAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = AssetType
            fields = (
                "id",
                "name",
                "description",
            )

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=200, required=False)
        description = serializers.CharField(max_length=200, required=False)

        class Meta:
            model = AssetType
            fields = (
                "name",
                "description",
            )

    UpdateOutputSerializer = OutputSerializer
    lookup_url_kwarg = "asset_type_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = AssetType.objects.all()
        qs = qs.filter(id=self.kwargs["asset_type_id"])
        return qs

    def get(self, request, *args, **kwargs):
        asset_type = self.get_object()
        resp_data = self.OutputSerializer(asset_type).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        asset_type = self.get_object()
        serializer = self.InputSerializer(instance=asset_type, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        asset_type = update_asset_type(asset_type, data)
        resp_data = self.UpdateOutputSerializer(asset_type).data
        return self.success_response(resp_data)

    def delete(self, request, *args, **kwargs):
        asset_type = self.get_object()
        deactivate_asset_type(asset_type)
        return self.success_response(
            data={"message": _("Asset Type is deactivated successfully")},
            status=status.HTTP_200_OK,
        )
