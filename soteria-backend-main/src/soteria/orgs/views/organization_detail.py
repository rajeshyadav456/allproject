from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import GenericAPIView
from soteria.models import Organization
from soteria.orgs.services.organization_detail import update_organization_detail


class OrganizationDetailGetUpdateAPI(GenericAPIView):
    class GetOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organization
            fields = (
                "id",
                "name",
                "slug",
                "status",
                "address",
                "updated_at",
                "created_at",
            )

    class UpdateInputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
        slug = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
        address = serializers.CharField(max_length=100, allow_blank=True)

        class Meta:
            model = Organization
            fields = (
                "name",
                "slug",
                "address",
            )

    UpdateOutputSerializer = GetOutputSerializer
    queryset = Organization.objects.all()
    lookup_url_kwarg = "organization_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(id=self.kwargs["organization_id"])
        return qs

    def get(self, request, *args, **kwargs):
        organization: Organization = self.get_object()
        resp_data = self.GetOutputSerializer(organization).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        organization: Organization = self.get_object()

        serializer = self.UpdateInputSerializer(
            instance=organization, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        organization = update_organization_detail(organization, data)
        resp_data = self.UpdateOutputSerializer(organization).data
        return self.success_response(resp_data)
