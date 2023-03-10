import logging
from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.core.validators import validate_email
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from soteria import roles
from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.utils import sane_repr, sane_str
from soteria.models import User, UserOrganization
from soteria.orgs.constants import ORGANIZATION_MEMBER_INVITE_VALIDITY_DAYS
from soteria.utils.urls import build_app_absolute_uri

logger = logging.getLogger(__name__)


class OrganizationMember(UserOrganization, DefaultFieldsModel):
    email = models.EmailField(
        blank=True, validators=[validate_email], verbose_name=_("email address")
    )
    mobile = models.CharField(
        max_length=18,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("mobile number"),
    )
    token = models.CharField(
        max_length=64, null=True, blank=True, db_index=True, verbose_name=_("token")
    )
    token_expires_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name=_("token expires at")
    )
    role = models.CharField(
        max_length=30,
        choices=roles.get_choices(),
        default=roles.get_default().id,
        verbose_name=_("role"),
    )
    location = models.ManyToManyField(
        "soteria_orgs.Location",
        through="OrganizationMemberLocation",
        blank=True,
        verbose_name=_("location"),
    )

    class Meta:
        app_label = "soteria_orgs"
        db_table = "soteria_org_member"
        verbose_name = _("organization member")
        verbose_name_plural = _("organization members")

    __repr__ = sane_repr("id", "organization_id", "user_id")
    __str__ = sane_str("id", "organization_id", "user_id")

    @property
    def is_user_exist(self):
        if not hasattr(self, "_user_exist"):
            self._user_exist = User.objects.filter(email__iexact=self.email).exists()
        return self._user_exist

    def get_email(self):
        if self.user_id and self.user.email:
            return self.user.email
        return self.email

    def generate_token(self):
        return uuid4().hex + uuid4().hex

    def refresh_expires_at(self):
        now = timezone.now()
        self.token_expires_at = now + timedelta(days=ORGANIZATION_MEMBER_INVITE_VALIDITY_DAYS)

    def get_role_name(self):
        return roles.get(self.role).name

    def get_invite_link(self):
        return build_app_absolute_uri(
            settings.ORG_MEMBER_INVITE_URL_PATH,
            query_params={
                "token": self.token,
                "email": self.get_email(),
                "mobile": self.mobile,
                "signup": not self.is_user_exist,
            },
        )

    def send_invite_notification(self):
        from soteria.core.notification import (
            OrganizationExistingMemberNotification,
            OrganizationNewMemberNotification,
        )

        self.token = self.generate_token()
        self.refresh_expires_at()
        self.save(update_fields=["token", "token_expires_at"])
        context = {
            "user_email": self.email,
            "organization": self.organization,
            "role": self.get_role_name(),
            "url": self.get_invite_link(),
            "url_expiry_days": ORGANIZATION_MEMBER_INVITE_VALIDITY_DAYS,
        }
        if self.is_user_exist:
            notification = OrganizationExistingMemberNotification(self, context=context)
        else:
            notification = OrganizationNewMemberNotification(self, context=context)

        try:
            member_email = self.get_email()
            notification.send_email(member_email)
            logger.info(f"{self.organization} invite mail sent to user {member_email}")
        except Exception as e:
            logger.exception(e)

    @transaction.atomic
    def set_locations(self, locations):
        from soteria.orgs.models import OrganizationMemberLocation

        # delete older and existing loctaion membership
        OrganizationMemberLocation.objects.all().filter(member=self).delete()

        # add to new locations
        self.add_to_locations(locations)

    def add_to_locations(self, locations):
        from soteria.orgs.models import OrganizationMemberLocation

        OrganizationMemberLocation.objects.bulk_create(
            [OrganizationMemberLocation(location=location, member=self) for location in locations]
        )

    def set_user(self, user):
        self.user = user
        self.token = None
        self.token_expires_at = None
        self.save(update_fields=["user", "token", "token_expires_at"])

    def get_permissions(self):
        """
        Returns a set of permissions user
        :return:
        """
        if not self.user:
            return {}
        perms = self.user.get_all_permissions()

        return perms

    def get_role(self):
        return roles.get(self.role)


class OrganizationMemberLocation(UUIDModel, DefaultFieldsModel):
    is_active = models.BooleanField(default=True)
    member = models.ForeignKey(OrganizationMember, on_delete=models.CASCADE)
    location = models.ForeignKey("soteria_orgs.Location", on_delete=models.CASCADE)

    class Meta:
        app_label = "soteria_orgs"
        db_table = "soteria_org_member_location"
        verbose_name = _("organization member location")
        verbose_name_plural = _("organization member locations")

    __repr__ = sane_repr("id", "member_id", "location_id")
    __str__ = sane_str("id", "member_id", "location_id")
