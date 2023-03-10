from typing import Dict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.atms.models import Asset


def update_asset_details(asset: Asset, data: Dict):
    name = data.get("name")
    if Asset.objects.filter(name=name).exists():
        raise serializers.ValidationError(_("Asset with same already exists."))

    update_fields = []

    asset_type = data.pop("asset_type_id", None)
    if asset_type:
        asset.asset_type = asset_type
        update_fields.append("asset_type")
    location = data.pop("location_id", None)
    if location:
        asset.location = location
        update_fields.append("location")

    for field, value in data.items():
        setattr(asset, field, value)
        update_fields.append(field)

    if update_fields:
        asset.save(update_fields=update_fields)

    return asset


def deactivate_asset(asset: Asset):
    Asset.objects.filter(id=asset.id).delete()
