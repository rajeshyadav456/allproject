from django_filters import rest_framework as dj_filters
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import MethodSerializerMixin, TenantAPIView
from soteria.atms.models import Asset, AssetType, Floor
from soteria.atms.serializers.assets import AssetTypeDetailSerializer
from soteria.atms.services.asset import create_asset, create_asset_qr
from soteria.orgs.models import Location


class AssetListCreateAPI(PaginatedListAPIViewMixin, MethodSerializerMixin, TenantAPIView):
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
                "location",
                "location_metadata",
                "tag",
                "image_url",
                "qr_data",
            )

        def get_qr_data(self, obj: Asset):
            return create_asset_qr(obj)

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=200)
        tag = serializers.CharField(max_length=100, required=False)
        floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all(), required=False)
        asset_type_id = serializers.PrimaryKeyRelatedField(
            queryset=AssetType.objects.all(), required=False
        )
        location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
        image_url = serializers.CharField(required=False, allow_null=True)
        location_metadata = serializers.CharField(required=False, allow_blank=True, allow_null=True)

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

    class ListPagination(DefaultPageNumberPagination):
        pass

    class ListFilterSet(dj_filters.FilterSet):
        name = dj_filters.CharFilter(field_name="name", lookup_expr="contains")
        location = dj_filters.ModelChoiceFilter(queryset=Location.objects.all())

        class Meta:
            model = Asset
            fields = ["tag"]

    ListOutputSerializer = OutputSerializer

    method_serializer_classes = {
        ("GET",): ListOutputSerializer,
        ("POST",): InputSerializer,
    }
    pagination_class = ListPagination
    queryset = Asset.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        dj_filters.DjangoFilterBackend,
    ]
    filterset_class = ListFilterSet

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        asset = create_asset(
            asset_name=data["name"],
            location=data["location_id"],
            tag=data.get("tag"),
            asset_type=data.get("asset_type_id"),
            floor=data.get("floor"),
            image_url=data.get("image_url"),
            location_metadata=data.get("location_metadata"),
        )
        resp_data = self.OutputSerializer(asset).data
        return self.success_response(data=resp_data, status=status.HTTP_201_CREATED)
