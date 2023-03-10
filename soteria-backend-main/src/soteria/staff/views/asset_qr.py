import json

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.utils.crypto import decrypt


class AssetQRDataAPI(TenantAPIView):
    class InputSerializer(serializers.Serializer):
        qr_data = serializers.CharField()

    serializer_class = InputSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        qr_dec_data = json.loads(decrypt(data["qr_data"]))
        return self.success_response(qr_dec_data)
