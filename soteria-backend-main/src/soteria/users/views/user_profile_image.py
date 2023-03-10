from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from soteria.api.file_upload import UploadedFileConfig
from soteria.api.views import GenericAPIView
from soteria.models import User
from soteria.users.services.user_profile_image import upload_user_profile


class UploadProfileImageAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        file = serializers.ImageField()

        def validate(self, attrs):
            file_config = UploadedFileConfig(file_type="image")
            field = file_config.get_serializer_field()
            field.run_validation(attrs["file"])
            return attrs

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = upload_user_profile(serializer.validated_data["file"], user)
        return self.success_response(data={"url": url})
