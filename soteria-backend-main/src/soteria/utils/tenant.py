from django.db import connection
from django_tenants.utils import get_public_schema_name

from soteria.models import Organization


def set_schema_connection(organization: Organization):
    """
    Method to set db `connection` to specfic tenant i.e organization.
    :As we not using `TenantAPIView` in some Views .
    """
    if organization.schema_name == get_public_schema_name():
        raise Exception("can not set It is a default `connection`.")
    connection.set_tenant(organization)
