from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import GenericAPIView
from soteria.models import Organization, User
from soteria.orgs.serializers.organization_detail import OrganizationDetailOutputSerializer
from soteria.orgs.services.organization import create_organization_and_member
from soteria.reports.services.template_report import create_report_templates


class OrganizationCreateAPI(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=50)
        slug = serializers.CharField(max_length=50)
        address = serializers.CharField(max_length=100)
        domain = serializers.CharField(max_length=50)

        def validate(self, attrs):
            attrs = super().validate(attrs)
            if Organization.objects.filter(slug=attrs["slug"]).exists():
                raise serializers.ValidationError(_("Organization with this slug already exists"))
            if Organization.objects.filter(name=attrs["name"]).exists():
                raise serializers.ValidationError(_("Organization with this name already exists"))
            return attrs

    serializer_class = InputSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        user: User = request.user
        organization, organization_member = create_organization_and_member(
            name=data["name"],
            slug=data["slug"],
            address=data["address"],
            domain=data["domain"],
            user=user,
        )
        create_report_templates(organization.id)
        resp_data = OrganizationDetailOutputSerializer(instance=organization).data
        return self.success_response(
            data=resp_data,
            status=status.HTTP_201_CREATED,
        )
