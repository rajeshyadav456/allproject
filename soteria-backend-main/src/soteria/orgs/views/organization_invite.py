from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.orgs.models import OrganizationMember
from soteria.orgs.services.organization_invite import accept_organization_member_invite


class OrganizationInviteAcceptAPI(TenantAPIView):
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
        token = serializers.CharField(max_length=80)

        class Meta:
            model = OrganizationMember
            fields = ("token",)

    permission_classes = (IsAuthenticated,)
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        org_member = accept_organization_member_invite(token=data["token"], user=user)
        resp_data = self.OutputSerializer(org_member).data
        return self.success_response(data=resp_data, status=status.HTTP_200_OK)
