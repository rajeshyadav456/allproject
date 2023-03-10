from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from soteria.models import Organization


class IsAuthorizedOrganizationPermissions(DjangoModelPermissions):
    """
    Allows access only to authorized users who have all permissions
    defined for each HTTP method in below default map or overridden in view
    for an organization as per role assigned to that user.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        if not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only
        ):
            return False

        queryset = self._queryset(view)
        required_perms = self.get_required_permissions(request.method, model_cls=queryset.model)
        organization = Organization.objects.filter(
            id=request.headers.get("x-organization-id")
        ).first()
        if not organization:
            return False

        # get all user permissions
        user_perms = request.user.get_all_permissions()

        # get user's organization specific permissions based on role
        org_member = request.user.get_org_member(organization)
        user_org_perms = set()
        if org_member:
            user_org_perms = org_member.get_permissions()
        request.organization_member = org_member
        user_perms = user_perms.union(user_org_perms)
        has_permission = all(perm in user_perms for perm in required_perms)
        return has_permission


class OrganizationPermissionMixin(object):
    def get_permissions(self):
        perms: list = super().get_permissions()
        perms.insert(0, IsAuthenticated())
        perms.insert(0, IsAuthorizedOrganizationPermissions())
        return perms
