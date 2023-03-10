from typing import Dict

from soteria import roles
from soteria.orgs.models import OrganizationMember
from soteria.sync_permission import sync_user_permissions


def update_organization_member_detail(org_member: OrganizationMember, data: Dict):
    """
    Update organziation member details.
    """
    locations = data.pop("locations", None)
    if locations:
        org_member.set_locations(locations)

    update_fields = []
    role: str = data.get("role")
    if role:
        sync_user_permissions(org_member.user, roles.get(role))

    for field, value in data.items():
        setattr(org_member, field, value)
        update_fields.append(field)

    if update_fields:
        org_member.save(update_fields=update_fields)

    return org_member


def deactivate_organization_member(org_member: OrganizationMember):
    """
    Deactivate organization member
    """

    OrganizationMember.objects.filter(id=org_member.id).delete()
