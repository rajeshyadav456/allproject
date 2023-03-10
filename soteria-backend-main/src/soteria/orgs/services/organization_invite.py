from django.utils import timezone
from rest_framework import serializers

from soteria.models import User
from soteria.orgs.models import OrganizationMember
from soteria.sync_permission import sync_user_permissions


def accept_organization_member_invite(token: str, user: User):
    """
    Accept organization member invitation .
    :link user to organization member

    """

    org_member = OrganizationMember.objects.filter(token=token).first()
    if not org_member:
        raise serializers.ValidationError("Not a Valid Token")
    if org_member.token_expires_at < timezone.now():
        raise serializers.ValidationError("Token Expires.")
    if org_member.email.lower() != user.email.lower():
        raise serializers.ValidationError("Invalid token for user")

    org_member.set_user(user)
    sync_user_permissions(user, org_member.get_role())
    return org_member
