from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.utils import sane_repr, sane_str


class AssetType(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("name"))
    description = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("description")
    )

    class Meta:
        app_label = "soteria_atms"
        db_table = "soteria_atms_asset_type"
        verbose_name = _("asset type")
        verbose_name_plural = _("asset types")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")


class Asset(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    asset_type = models.ForeignKey(
        "soteria_atms.AssetType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("asset type"),
    )
    floor = models.ForeignKey(
        "soteria_atms.Floor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("floor"),
    )
    location = models.ForeignKey(
        "soteria_orgs.Location",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("location"),
    )
    location_metadata = models.CharField(
        max_length=100, blank=True, verbose_name=_("location metadata")
    )
    tag = models.CharField(max_length=100, blank=True, verbose_name=_("tag"))
    image_url = models.CharField(_("image url"), max_length=200, null=True, blank=True)

    class Meta:
        app_label = "soteria_atms"
        db_table = "soteria_atms_asset"
        verbose_name = _("asset")
        verbose_name_plural = _("assets")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")
