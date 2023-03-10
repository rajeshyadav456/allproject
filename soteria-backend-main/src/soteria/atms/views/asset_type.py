from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import MethodSerializerMixin, TenantAPIView
from soteria.atms.models import AssetType
from soteria.atms.services.asset_type import create_asset_type


class AssetTypeListCreateAPI(
    PaginatedListAPIViewMixin,
    MethodSerializerMixin,
    TenantAPIView,
):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = AssetType
            fields = (
                "id",
                "name",
                "description",
            )

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=100)
        description = serializers.CharField(max_length=200, required=False)

        class Meta:
            model = AssetType
            fields = ("name", "description")

    class ListPagination(DefaultPageNumberPagination):
        page_size = 30

    ListOutputSerializer = OutputSerializer

    method_serializer_classes = {
        ("GET",): ListOutputSerializer,
        ("POST",): InputSerializer,
    }
    pagination_class = ListPagination
    queryset = AssetType.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        asset_type = create_asset_type(name=data["name"], description=data.get("description"))
        resp_data = self.OutputSerializer(asset_type).data
        return self.success_response(data=resp_data, status=status.HTTP_201_CREATED)
