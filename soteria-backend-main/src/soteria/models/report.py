from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import TimeStampedModel
from soteria.db.models.utils import sane_repr, sane_str
from soteria.models import Organization


class Report(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("name"))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    column_mapping = models.JSONField()
    included_columns = models.JSONField()

    class Meta:
        app_label = "soteria"
        db_table = "soteria_report"

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")
