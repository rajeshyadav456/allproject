from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.orgs.models import Location, OrganizationMember
from soteria.orgs.serializers.organizatioin_member import OrganizationMemberRoleSerializer
from soteria.orgs.services.organization_member_detail import (
    deactivate_organization_member,
    update_organization_member_detail,
)
from soteria.orgs.views.base.view import OrganizationAPIMixin


class OrganizationMemberGetUpdateDeleteAPI(
    TenantAPIView,
    OrganizationAPIMixin,
):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrganizationMember
            fields = (
                "id",
                "email",
                "mobile",
                "role",
                "organization",
            )

    class InputSerializer(serializers.ModelSerializer):
        role = OrganizationMemberRoleSerializer()
        locations = serializers.PrimaryKeyRelatedField(
            queryset=Location.objects.all(), many=True, required=False
        )

        class Meta:
            model = OrganizationMember
            fields = (
                "role",
                "locations",
            )

    UpdateOutputSerializer = OutputSerializer
    lookup_url_kwarg = "member_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = OrganizationMember.objects.all()
        qs = qs.filter(id=self.kwargs["member_id"], organization=self.organization)
        return qs

    def get(self, request, *args, **kwargs):
        org_member = self.get_object()
        resp_data = self.OutputSerializer(org_member).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        org_member = self.get_object()
        serializer = self.InputSerializer(instance=org_member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        org_member = update_organization_member_detail(org_member, data)
        resp_data = self.UpdateOutputSerializer(org_member).data
        return self.success_response(resp_data)

    def delete(self, request, *args, **kwargs):
        org_member = self.get_object()
        deactivate_organization_member(org_member)
        return self.success_response(
            data={"message": _("Organization member is deactivated successfully")},
            status=status.HTTP_200_OK,
        )
