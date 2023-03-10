import logging

from rest_framework import serializers

from soteria.api.views import GenericAPIView
from soteria.auth.service.refresh_token import get_access_token_from_refresh_token

logger = logging.getLogger(__name__)


class RefreshAccessTokenAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        refresh_token = serializers.CharField()

    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        refresh_token = data.pop("refresh_token")
        result = get_access_token_from_refresh_token(refresh_token)
        logger.info(f"New access token issued using refresh token")
        return self.success_response(result)
