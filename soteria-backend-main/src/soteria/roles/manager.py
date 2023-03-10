from collections import OrderedDict
from typing import List

from .role import Role


class RoleManager(object):
    def __init__(self, config, default=None):
        role_list = []
        self._roles = OrderedDict()
        self._role_ids = []
        for idx, role in enumerate(config):
            role = self.prepare_role({**role, "priority": idx})
            role_list.append(role)
            self._roles[role.id] = role
            self._role_ids.append(role.id)

        self._choices = tuple((r.id, r.name) for r in role_list)

        if default:
            self._default = self._roles[default]
        else:
            self._default = role_list[0]

        self._top_dog = role_list[-1]

    def __iter__(self):
        return iter(self._roles.values())

    def role_exists(self, role_id):
        return role_id in self._role_ids

    def can_manage(self, role, other):
        return self.get(role).priority >= self.get(other).priority

    def get(self, role_id) -> Role:
        return self._roles[role_id]

    def get_by_name(self, role_name) -> Role:
        for role in self.get_all():
            if role.name == role_name:
                return role

    def get_all(self) -> List[Role]:
        return list(self._roles.values())

    def get_choices(self):
        return self._choices

    def get_default(self) -> Role:
        return self._default

    def get_top_dog(self) -> Role:
        return self._top_dog

    def get_global_roles(self) -> List[Role]:
        global_roles = []
        for role in self.get_all():
            if role.is_global:
                global_roles.append(role)
        return global_roles

    def get_public_info_list(self):
        roles_public_info = []
        for role in self.get_all():
            roles_public_info.append(role.to_public_info())
        return roles_public_info

    def with_permission(self, permission):
        for role in self.get_all():
            if role.has_permission(permission):
                yield role

    def prepare_role(self, role_config) -> Role:
        priority = role_config.pop("priority", None)
        role_id = role_config.pop("role_id", None)
        name = role_config.pop("name", None)
        if priority is None:
            priority = self._role_ids.index(role_id)
        return Role(priority, role_id, name, **role_config)

    def get_permission_list(self, role_name) -> List:
        role = self.get_by_name(role_name)
        return role.permission_list()
