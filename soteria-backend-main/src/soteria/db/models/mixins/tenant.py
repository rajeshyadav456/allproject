from django_tenants.models import TenantMixin

from soteria.db.models.base import DefaultFieldsModel, UUIDModel


class TenantModelMixin(TenantMixin, UUIDModel, DefaultFieldsModel):
    pass
