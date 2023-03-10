import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria import roles
from soteria.models import Organization, User
from soteria.orgs.models import OrganizationMember

logger = logging.getLogger(__name__)


def create_organization(name: str, slug: str, address: str, domain: str, user: User):
    """
    Create organization
    """
    if not user.can_create_org:
        raise serializers.ValidationError(_("You not allowed to perform this action."))
    if Organization.objects.filter(schema_name=domain).exists():
        raise serializers.ValidationError(_("Domain name already registered."))
    organization = Organization.objects.create(
        schema_name=domain,
        name=name,
        slug=slug,
        address=address,
    )
    logger.info(f"Organization {organization} is successfully created")
    return organization


def create_organization_member(user: User, organization: Organization):
    """
    Create member for organization
    :who creates organization consider `Leader` for organization.
    """
    from soteria.utils.tenant import set_schema_connection

    # setting current tenant
    set_schema_connection(organization)
    if OrganizationMember.objects.filter(user=user).exists():
        raise serializers.ValidationError(_("User is already a member of organization."))
    organization_member = OrganizationMember.objects.create(
        email=user.email,
        mobile=user.mobile,
        user=user,
        role=roles.get_top_dog().id,
        organization=organization,
    )
    logger.info(f"Organization Member {organization_member} is created.")
    return organization_member


def create_organization_and_member(name: str, slug: str, address: str, domain: str, user: User):
    """
    User can create only one organization
    """
    with transaction.atomic():
        organization = create_organization(
            name=name, slug=slug, address=address, domain=domain, user=user
        )
        organization_member = create_organization_member(user=user, organization=organization)
        return organization, organization_member
