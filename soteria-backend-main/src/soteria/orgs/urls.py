from django.urls import path

from soteria.orgs.views.location import LocationListCreateAPI
from soteria.orgs.views.location_detail import LocationDetailGetUpdateAPI
from soteria.orgs.views.organization import OrganizationCreateAPI
from soteria.orgs.views.organization_detail import OrganizationDetailGetUpdateAPI
from soteria.orgs.views.organization_invite import OrganizationInviteAcceptAPI
from soteria.orgs.views.organization_member import OrganizationMemberListCreateAPI
from soteria.orgs.views.orgnization_member_detail import OrganizationMemberGetUpdateDeleteAPI
from soteria.orgs.views.user_organization import UserOrganizationListAPI

urlpatterns = [
    path("api/v1/organizations/", OrganizationCreateAPI.as_view(), name="create-organizations"),
    path(
        "api/v1/me/organizations/",
        UserOrganizationListAPI.as_view(),
        name="user-organizations-list",
    ),
    path(
        "api/v1/organizations/<uuid:organization_id>/",
        OrganizationDetailGetUpdateAPI.as_view(),
        name="organization-details",
    ),
    path(
        "api/v1/organizations/<uuid:organization_id>/locations/",
        LocationListCreateAPI.as_view(),
        name="organization-locations",
    ),
    path(
        "api/v1/organizations/<uuid:organization_id>/locations/<uuid:location_id>/",
        LocationDetailGetUpdateAPI.as_view(),
        name="organization-location-details",
    ),
    path(
        "api/v1/organizations/<uuid:organization_id>/members/",
        OrganizationMemberListCreateAPI.as_view(),
        name="organization-members",
    ),
    path(
        "api/v1/organizations/members/accept-invite/",
        OrganizationInviteAcceptAPI.as_view(),
        name="organization-member-accept-invite",
    ),
    path(
        "api/v1/organizations/<uuid:organization_id>/members/<uuid:member_id>/",
        OrganizationMemberGetUpdateDeleteAPI.as_view(),
        name="organization-member-details",
    ),
]
