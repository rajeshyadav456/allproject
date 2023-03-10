import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.models import Organization
from soteria.orgs.models import Location

logger = logging.getLogger(__name__)


def create_location_for_organization(
    name: str, address: str, city: str, organization: Organization
):
    """
    Create Location for Organization
    :Each location created in their respective organization schema.
    """
    if not organization.status == Organization.Status.ACTIVE:
        raise serializers.ValidationError(_("Organization is not active"))

    if Location.objects.filter(name=name, organization=organization).exists():
        raise serializers.ValidationError(_("Location with same name already exists."))

    location = Location.objects.create(
        name=name, address=address, city=city, organization=organization
    )
    logger.info(f"Location {location} is created for organization {organization}")
    return location
