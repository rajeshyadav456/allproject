from typing import Dict

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.orgs.models import Location


def update_location_detail(location: Location, data: Dict):
    """
    Update location detail.
    """

    name = data.get("name")
    if Location.objects.filter(name=name).exists():
        raise serializers.ValidationError(_("Location name already exists."))

    update_fields = []

    for field, value in data.items():
        setattr(location, field, value)
        update_fields.append(field)

    if update_fields:
        location.save(update_fields=update_fields)

    return location


@transaction.atomic()
def deactivate_location(location: Location):
    """
    Deactivate Location
    """

    Location.objects.filter(id=location.id).delete()
