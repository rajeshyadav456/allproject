import base64
import json
from io import BytesIO

import qrcode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.atms.models import Asset, AssetType, Floor
from soteria.orgs.models import Location
from soteria.utils import crypto


def create_asset(
    asset_name: str,
    location: Location,
    tag: str = None,
    asset_type: AssetType = None,
    floor: Floor = None,
    image_url: str = None,
    location_metadata: str = None,
) -> Asset:

    if Asset.objects.filter(name=asset_name).exists():
        raise serializers.ValidationError(_("Asset with same name already exists."))

    # creating asset only for a location
    asset = Asset.objects.create(
        name=asset_name,
        asset_type=asset_type,
        location=location,
        floor=floor,
        tag=tag,
        image_url=image_url,
        location_metadata=location_metadata,
    )

    return asset


def create_asset_qr(asset: Asset):
    """
    Create QR image file like object
    : retruns : image file in base64 bytes
    """
    data = {"asset_id": str(asset.id), "asset_name": asset.name}
    if asset.asset_type:
        data["asset_type"] = asset.asset_type.name
    if asset.location:
        data["location"] = asset.location.name
    if asset.floor:
        data["floor"] = asset.floor.name
    if asset.location_metadata:
        data["location_metadata"] = asset.location_metadata
    if asset.tag:
        data["tag"] = asset.tag
    if asset.image_url:
        data["image_url"] = asset.image_url

    data = json.dumps(data)
    qr = qrcode.QRCode(
        box_size=10,
        border=4,
    )
    en_data = crypto.encrypt(data)
    qr.add_data(en_data)
    img = qr.make_image(fill_color="black", back_color="white")
    image_file = BytesIO()
    img.save(image_file, format="png")
    image_file.seek(0)
    img_bytes = image_file.read()

    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    return base64_encoded_result_bytes
