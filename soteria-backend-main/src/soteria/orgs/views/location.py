from rest_framework import serializers, status

from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import MethodSerializerMixin, TenantAPIView
from soteria.orgs.models import Location
from soteria.orgs.services.location import create_location_for_organization
from soteria.orgs.views.base.view import OrganizationAPIMixin


class LocationListCreateAPI(
    PaginatedListAPIViewMixin,
    OrganizationAPIMixin,
    MethodSerializerMixin,
    TenantAPIView,
):
    class CreateInputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=100)
        city = serializers.CharField(max_length=50)
        address = serializers.CharField(max_length=100)

        class Meta:
            model = Location
            fields = (
                "name",
                "city",
                "address",
            )

    class CreateOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Location
            fields = [
                "id",
                "name",
                "slug",
                "status",
                "city",
                "address",
                "updated_at",
                "created_at",
            ]

    class ListPagination(DefaultPageNumberPagination):
        pass

    ListOutputSerializer = CreateOutputSerializer

    method_serializer_classes = {
        ("GET",): ListOutputSerializer,
        ("POST",): CreateInputSerializer,
    }
    pagination_class = ListPagination
    queryset = Location.objects.all().order_by("-created_at")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(organization=self.organization)
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        location = create_location_for_organization(
            name=data["name"],
            address=data["address"],
            city=data["city"],
            organization=self.organization,
        )
        resp_data = self.CreateOutputSerializer(location).data
        return self.success_response(data=resp_data, status=status.HTTP_201_CREATED)
