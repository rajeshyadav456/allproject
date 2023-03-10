from django.db import connection
from django_tenants.middleware.main import TenantMainMiddleware
from django_tenants.utils import get_tenant_domain_model

from soteria.models import Organization


class OrganizationHeaderMiddleware(TenantMainMiddleware):
    def process_request(self, request):
        """
        This middleware Extends the default behavior of
        `django_tenants.middleware.main.TenantMainMiddleware`
        :when `HTTP_X_ORGANIZATION_ID` is present in request
        Then the connection set Tenant for that org_id.
        """

        org_id = request.headers.get("X-ORGANIZATION-ID")
        if org_id:
            try:
                organization = Organization.objects.get(id=org_id)
            except Organization.DoesNotExist:
                raise self.TENANT_NOT_FOUND_EXCEPTION("Invalid Tenant")

            request.organization = organization
            connection.set_tenant(request.organization)
            return

        # setting tenant using domain
        connection.set_schema_to_public()
        hostname = self.hostname_from_request(request)
        domain_model = get_tenant_domain_model()
        try:
            organization = self.get_tenant(domain_model, hostname)
        except domain_model.DoesNotExist:
            self.no_tenant_found(request, hostname)
            return
        organization.domain_url = hostname
        request.organization = organization
        connection.set_tenant(request.organization)
        self.setup_url_routing(request)
