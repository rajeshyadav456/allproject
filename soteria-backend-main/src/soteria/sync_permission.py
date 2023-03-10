from typing import List

from django.contrib.auth.models import Permission

from soteria.models import User
from soteria.roles.manager import Role

# a mapping of codename => permission
perms_cname_map = {}


def _load_perms_cname_map():
    global perms_cname_map
    # a mapping of codename => permission
    perms_cname_map = {p.codename: p for p in Permission.objects.all()}


def get_permission(codename) -> Permission:
    if not perms_cname_map:
        _load_perms_cname_map()
    return perms_cname_map.get(codename)


def get_permissions(codenames, exists_only=False) -> List[Permission]:
    permissions = []
    for codename in codenames:
        permission = get_permission(codename)
        if exists_only and not permission:
            continue
        permissions.append(permission)
    return permissions


def sync_user_permissions(user: User, role: Role):

    perm_exist_cnames = set(user.user_permissions.values_list("codename", flat=True).all())
    # already a frozenset
    perm_required_cnames = role.permission_list()

    # add missing permissions to user
    perm_missing_cnames = perm_required_cnames.difference(perm_exist_cnames)
    perms_missing = get_permissions(perm_missing_cnames, exists_only=True)
    if perms_missing:
        user.user_permissions.set(perms_missing)

    # remove permissions from user not required anymore
    perm_remove_cnames = perm_exist_cnames.difference(perm_required_cnames)
    perms_remove = get_permissions(perm_remove_cnames, exists_only=True)
    if perms_remove:
        user.user_permissions.remove(*perms_remove)
