from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import DefaultFieldsModel
from soteria.db.models.utils import sane_repr, sane_str


class InvitationCode(DefaultFieldsModel):
    code = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    user = models.OneToOneField(
        "soteria.User", null=True, blank=True, editable=False, on_delete=models.SET_NULL
    )

    class Meta:
        app_label = "soteria"
        db_table = "soteria_invitation_code"
        verbose_name = _("invitation code")
        verbose_name_plural = _("invitation codes")

    __repr__ = sane_repr("id", "user_id")
    __str__ = sane_str("id", "user_id")

    @classmethod
    def create_for_org_member(cls, org_member):
        if not org_member.token:
            raise Exception(f"'token' is not set of <{org_member}>")
        return cls.objects.create(code=org_member.token)

    def belongs_to_invited_org_member(self) -> bool:
        """
        When we invite a new user to org we also create a signup invitation
        code with same value as org invitation token.

        If we found any user having same token as given code, then this
        signup invitation code belongs to invited org member.
        :return:
        """
        from soteria.orgs.models import OrganizationMember

        return OrganizationMember.objects.filter(token=self.code).exists()
