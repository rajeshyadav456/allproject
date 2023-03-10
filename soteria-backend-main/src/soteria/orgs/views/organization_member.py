from django_filters import rest_framework as dj_filters
from rest_framework import serializers, status

from soteria import roles
from soteria.api.fields import EmailSerializerField, MobileNumberField
from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import MethodSerializerMixin, TenantAPIView
from soteria.orgs.models import Location, OrganizationMember
from soteria.orgs.serializers.organizatioin_member import OrganizationMemberRoleSerializer
from soteria.orgs.serializers.user import UserSerializer
from soteria.orgs.services.organization_member import create_organization_member
from soteria.orgs.views.base.view import OrganizationAPIMixin
from soteria.permissions import OrganizationPermissionMixin


class OrganizationMemberListCreateAPI(
    OrganizationPermissionMixin,
    PaginatedListAPIViewMixin,
    MethodSerializerMixin,
    OrganizationAPIMixin,
    TenantAPIView,
):
    class OutputSerializer(serializers.ModelSerializer):
        role = OrganizationMemberRoleSerializer()
        user = UserSerializer()

        class Meta:
            model = OrganizationMember
            fields = (
                "id",
                "email",
                "mobile",
                "role",
                "user",
            )

    class InputSerializer(serializers.ModelSerializer):
        email = EmailSerializerField(allow_blank=True)
        mobile = MobileNumberField()
        role = OrganizationMemberRoleSerializer()
        locations = serializers.PrimaryKeyRelatedField(
            queryset=Location.objects.all(), many=True, required=False
        )

        class Meta:
            model = OrganizationMember
            fields = ("email", "mobile", "role", "locations")

        def validate(self, attrs):
            role = attrs["role"]
            if roles.get(role) == roles.get_by_name("Staff"):
                if attrs["email"] != "":
                    raise serializers.ValidationError(f"For staff role email should be blank.")
            else:
                if attrs["email"] == "":
                    raise serializers.ValidationError("Email is required.")

            return attrs

    class ListFilterSet(dj_filters.FilterSet):
        location = dj_filters.ModelChoiceFilter(queryset=Location.objects.all())

        class Meta:
            model = OrganizationMember
            fields = ["role", "email", "mobile"]

    class ListPagination(DefaultPageNumberPagination):
        pass

    ListOutputSerializer = OutputSerializer

    method_serializer_classes = {
        ("GET",): ListOutputSerializer,
        ("POST",): InputSerializer,
    }
    pagination_class = ListPagination
    queryset = OrganizationMember.objects.all().order_by("-created_at")
    filter_backends = [
        dj_filters.DjangoFilterBackend,
    ]
    filter_class = ListFilterSet

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
        org_member = create_organization_member(
            organization=self.organization,
            role=data["role"],
            email=data["email"],
            mobile=data["mobile"],
            locations=data.get("locations"),
        )
        resp_data = self.OutputSerializer(org_member).data
        return self.success_response(data=resp_data, status=status.HTTP_201_CREATED)
