from typing import Dict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.atms.models import AssetType


def create_asset_type(name: str, description: str = None):
    if AssetType.objects.filter(name=name).exists():
        raise serializers.ValidationError(_("Asset Type with same name already exists."))
    asset_type = AssetType.objects.create(name=name, description=description)
    return asset_type


def update_asset_type(asset_type: AssetType, data: Dict):
    if AssetType.objects.filter(name=data.get("name")).exists():
        raise serializers.ValidationError(_("Asset Type with same name already exists."))

    update_fields = []
    for field, value in data.items():
        setattr(asset_type, field, value)
        update_fields.append(field)

    if update_fields:
        asset_type.save(update_fields=update_fields)

    return asset_type


def deactivate_asset_type(asset_type: AssetType):
    AssetType.objects.filter(id=asset_type.id).delete()
