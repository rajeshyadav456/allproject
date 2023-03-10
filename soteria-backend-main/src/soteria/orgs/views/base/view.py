from django.utils.functional import cached_property
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from soteria.models import Organization


class OrganizationAPIMixin:
    """Base view class for url path starts with `organizations/<uuid:organization_id>/`

    For example:
      * `organization/<uuid:organization_id>/locations/`
    """

    permission_classes = (IsAuthenticated,)

    @cached_property
    def organization(self):
        """Return organization instance"""
        filter_kwargs = {"id": self.kwargs["organization_id"]}
        return get_object_or_404(Organization.objects.all(), **filter_kwargs)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()

        if "organization_id" in self.kwargs:
            ctx["organization_id"] = self.organization

        return ctx
