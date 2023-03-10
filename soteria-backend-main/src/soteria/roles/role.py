class Role(object):
    def __init__(
        self,
        priority,
        role_id,
        name,
        is_global=False,
        short_desc="",
        permissions=None,
        can_access_dashboard=True,
    ):
        assert len(role_id) <= 32, "Role id must be no more than 32 characters"

        self.priority = priority
        self.id = role_id
        self.name = name
        self.short_description = short_desc
        self.permissions = frozenset(permissions or [])
        self.can_access_dashboard = bool(can_access_dashboard)
        self.is_global = bool(is_global)

    def __str__(self):
        return self.name.encode("utf-8")

    def __unicode__(self):
        return str(self.name)

    def __repr__(self):
        return "<Role: {}>".format(self.id)

    def has_permission(self, perm):
        return perm in self.permissions

    def permission_list(self):
        return self.permissions

    def to_public_info(self):
        return {
            "id": self.id,
            "role_id": self.id,
            "name": self.name,
            "is_global": self.is_global,
            "can_access_dashboard": self.can_access_dashboard,
            "short_description": self.short_description,
            "permission_list": self.permissions,
        }
