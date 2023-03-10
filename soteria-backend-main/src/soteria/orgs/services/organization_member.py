import logging
from typing import List

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria import roles
from soteria.models import InvitationCode, Organization, User
from soteria.orgs.models import Location, OrganizationMember
from soteria.roles.role import Role
from soteria.sync_permission import sync_user_permissions

logger = logging.getLogger(__name__)


@transaction.atomic()
def create_organization_member(
    organization: Organization,
    role: Role,
    email: str,
    mobile: str,
    locations: List[Location] = [],
):
    role = roles.get(role)
    if not organization.status == Organization.Status.ACTIVE:
        raise serializers.ValidationError(_("Organization is not active"))

    if OrganizationMember.objects.filter(mobile=mobile).exists():
        raise serializers.ValidationError(_("Member with mobile already exists."))
    # Intentionally we doing check in diff query for email and mobile
    # for staff we store email as blank
    if OrganizationMember.objects.filter(email=email).exists() and not (
        role is roles.get_by_name("Staff")
    ):
        raise serializers.ValidationError(_("Member with email already exists."))

    if roles.get_by_name("Staff") == role:
        # for staff only mobile is mandatory
        email = ""

    org_member: OrganizationMember = OrganizationMember.objects.create(
        email=email,
        mobile=mobile,
        role=role.id,
        organization=organization,
    )
    if not role.is_global:
        org_member.set_locations(locations)

    if role == roles.get_by_name("Staff"):
        try:
            user = User.objects.create(
                first_name="",
                last_name="",
                email=email,
                mobile=mobile,
                username=mobile,
                can_create_org=False,
            )
            org_member.user = user
            org_member.save(update_fields=["user"])
            sync_user_permissions(user, role)

        except Exception as e:
            logger.exception(e)
            raise serializers.ValidationError(f"Unable to create user for role {role}")
    else:
        org_member.send_invite_notification()
        is_new_user = not User.objects.filter(email=org_member.email).exists()
        if is_new_user:
            InvitationCode.create_for_org_member(org_member)
    return org_member
