from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.utils import sane_repr, sane_str


class Floor(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=200, unique=True, verbose_name=_("name"))
    description = models.CharField(max_length=200, blank=True, verbose_name=_("description"))
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "soteria_atms"
        db_table = "soteria_atms_floor"
        verbose_name = _("floor")
        verbose_name_plural = _("floors")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")
