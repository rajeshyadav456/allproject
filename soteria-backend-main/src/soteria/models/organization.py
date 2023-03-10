from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tenants.models import DomainMixin

from soteria.db.models.mixins.tenant import TenantModelMixin
from soteria.db.models.utils import sane_repr, sane_str


class Organization(TenantModelMixin):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        INACTIVE = "inactive", _("Inactive")

    name = models.CharField(max_length=100, unique=True, verbose_name=_("name"))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_("slug"))
    status = models.CharField(
        max_length=100, choices=Status.choices, default=Status.ACTIVE, verbose_name=_("status")
    )
    address = models.CharField(max_length=200, blank=True, verbose_name=_("address"))

    class Meta:
        app_label = "soteria"
        db_table = "soteria_organization"
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")


class Domain(DomainMixin):
    domain_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = "soteria"
        db_table = "soteria_domain"
        verbose_name = _("domains")
        verbose_name_plural = _("domains")

    __repr__ = sane_repr("id", "domain_name")
    __str__ = sane_str("id", "domain_name")
