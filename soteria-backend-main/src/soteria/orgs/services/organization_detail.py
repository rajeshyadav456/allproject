from typing import Dict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.models import Organization


def update_organization_detail(organization: Organization, data: Dict):
    """
    Update organization detail
    """
    name = data.get("name")
    if Organization.objects.filter(name=name).exists():
        raise serializers.ValidationError(_("Organziation name already exists."))

    slug = data.get("slug")
    if Organization.objects.filter(slug=slug).exists():
        raise serializers.ValidationError(_("Slug name already exists"))

    update_fields = []

    for field, value in data.items():
        setattr(organization, field, value)
        update_fields.append(field)

    if update_fields:
        organization.save(update_fields=update_fields)

    return organization
