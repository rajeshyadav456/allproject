import json
from os import path

from django.conf import settings

from soteria.models import Organization


def load_roles_config_file(config_file):
    config_file_path = config_file
    ROLE_DIR = (settings.BASE_DIR / "..").resolve()
    if config_file == "roles.json":
        config_file_path = path.normpath(
            path.join(
                ROLE_DIR,
                "roles",
                config_file,
            )
        )

    with open(config_file_path, "r") as f:
        roles_config = json.load(f)
    return roles_config


def sync_org_users_permissions():
    organizations = Organization.objects.all().exclude(schema_name=settings.PUBLIC_SCHEMA_NAME)
    from soteria.orgs.models import OrganizationMember
    from soteria.sync_permission import sync_user_permissions
    from soteria.utils.tenant import set_schema_connection

    for org in organizations:
        set_schema_connection(org)
        org_members = OrganizationMember.objects.all()
        for org_member in org_members:
            if org_member.user:
                sync_user_permissions(org_member.user, org_member.get_role())
