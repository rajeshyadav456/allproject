from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.utils import sane_repr, sane_str


class Form(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    schema = models.JSONField(null=True, blank=True, verbose_name=_("schema"))

    class Meta:
        app_label = "soteria_atms"
        db_table = "soteria_atms_forms"
        verbose_name = _("forms")
        verbose_name_plural = _("forms")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")
