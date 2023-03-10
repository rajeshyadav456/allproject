from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import GenericAPIView
from soteria.models import User, UserOrganization
from soteria.orgs.serializers.organization_detail import OrganizationDetailOutputSerializer
from soteria.orgs.services.user_organization import get_pending_invites_org_for_user


class UserOrganizationListAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user: User = request.user
        user_all_orgs = UserOrganization.objects.filter(user=user).all()

        user_orgs = []
        for user_org in user_all_orgs:
            organization = user_org.organization
            org_data = OrganizationDetailOutputSerializer(organization).data
            user_orgs.append(org_data)

        pending_invites = get_pending_invites_org_for_user(user)

        return self.success_response(
            data={
                "organizations": user_orgs,
                "permissions": user.get_all_permissions(),
                "pending_invites": pending_invites,
            },
            status=status.HTTP_200_OK,
        )
