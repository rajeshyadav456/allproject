from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.mixins.slug_model import SlugModelMixin
from soteria.db.models.utils import sane_repr, sane_str


class Location(UUIDModel, SlugModelMixin, DefaultFieldsModel):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        INACTIVE = "inactive", _("Inactive")

    name = models.CharField(max_length=100, verbose_name=_("name"))
    address = models.CharField(max_length=100, blank=True, verbose_name=_("address"))
    status = models.CharField(
        max_length=100, choices=Status.choices, default=Status.ACTIVE, verbose_name=_("status")
    )
    city = models.CharField(max_length=100, blank=True, verbose_name=_("city"))
    organization = models.ForeignKey(
        "soteria.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("organization"),
    )

    class Meta:
        app_label = "soteria_orgs"
        db_table = "soteria_orgs_location"
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    SLUG_POPULATE_FROM = "name"

    __repr__ = sane_repr("id", "name", "status")
    __str__ = sane_str("id", "name", "status")
