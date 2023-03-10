from django.conf import settings

from soteria.models import Organization, User
from soteria.orgs.models import OrganizationMember
from soteria.orgs.serializers.organizatioin_member import OrganizationMemberDetailSerializer
from soteria.utils.tenant import set_schema_connection


def get_pending_invites_org_for_user(user: User):
    orgs = Organization.objects.all().exclude(schema_name=settings.PUBLIC_SCHEMA_NAME)
    pending_invites = []

    for org in orgs:
        set_schema_connection(org)
        org_member = (
            OrganizationMember.objects.filter(email=user.email, mobile=user.mobile)
            .exclude(user__isnull=False)
            .first()
        )
        if not org_member:
            continue
        org_member_detail = OrganizationMemberDetailSerializer(org_member).data
        pending_invites.append(org_member_detail)

    return pending_invites
