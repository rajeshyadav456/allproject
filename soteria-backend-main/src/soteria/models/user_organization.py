from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import UUIDModel
from soteria.db.models.utils import sane_repr, sane_str


class UserOrganization(UUIDModel):
    user = models.ForeignKey(
        "soteria.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    organization = models.ForeignKey(
        "soteria.Organization",
        on_delete=models.CASCADE,
        verbose_name=_("organization"),
    )

    class Meta:
        app_label = "soteria"
        db_table = "soteria_user_organization"
        verbose_name = _("user organization")
        verbose_name_plural = _("user organizations")

    __repr__ = sane_repr("id", "organization_id", "user_id")
    __str__ = sane_str("id", "organization_id", "user_id")
