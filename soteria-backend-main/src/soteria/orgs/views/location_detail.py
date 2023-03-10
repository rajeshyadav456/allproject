from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status

from soteria.api.views import TenantAPIView
from soteria.orgs.models import Location
from soteria.orgs.services.location_detail import deactivate_location, update_location_detail
from soteria.orgs.views.base.view import OrganizationAPIMixin


class LocationDetailGetUpdateAPI(OrganizationAPIMixin, TenantAPIView):
    class GetOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Location
            fields = (
                "id",
                "name",
                "slug",
                "status",
                "city",
                "address",
                "updated_at",
                "created_at",
            )

    class UpdateInputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
        city = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
        address = serializers.CharField(max_length=100, allow_blank=True)

        class Meta:
            model = Location
            fields = (
                "name",
                "city",
                "address",
            )

    UpdateOutputSerializer = GetOutputSerializer
    lookup_url_kwarg = "location_id"
    queryset = Location.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(id=self.kwargs["location_id"], organization=self.organization)
        return qs

    def get(self, request, *args, **kwargs):
        location: Location = self.get_object()
        resp_data = self.GetOutputSerializer(location).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        location: Location = self.get_object()

        serializer = self.UpdateInputSerializer(instance=location, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        location = update_location_detail(location, data)
        resp_data = self.UpdateOutputSerializer(location).data
        return self.success_response(resp_data)

    def delete(self, request, *args, **kwargs):
        location: Location = self.get_object()
        deactivate_location(location=location)
        return self.success_response(
            data={"message": _("Location is deactivated successfully")},
            status=status.HTTP_200_OK,
        )
