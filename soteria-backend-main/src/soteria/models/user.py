from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        blank=True, validators=[validate_email], verbose_name=_("email address")
    )
    email_verified = models.BooleanField(default=False, verbose_name=_("email verified"))
    mobile = models.CharField(
        max_length=18, null=True, blank=True, unique=True, verbose_name=_("mobile number")
    )
    mobile_verified = models.BooleanField(default=False, verbose_name=_("mobile verified"))
    avatar_url = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("avatar url")
    )
    can_create_org = models.BooleanField(
        default=False,
        verbose_name=_("can user create new organization"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_("last updated at")
    )
    updated_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("updated by"),
    )
    last_password_change_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("date of last password change"),
        help_text=_("The date the password was changed last."),
    )

    class Meta:
        app_label = "soteria"
        db_table = "soteria_user"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return f"User(id='{self.id}', email='{self.email}')"

    def save(self, *args, **kwargs):
        self.email = self.normalize_email(self.email)

        if not self.username:
            # username would be same as email, if not set
            self.username = self.email

        return super().save(*args, **kwargs)

    @classmethod
    def normalize_email(cls, email):
        email = cls.objects.normalize_email(email)
        # we will lowercase the email for case-insensitive matching
        return str(email).strip(" ").lower()

    def verify_email(self):
        if self.email_verified:
            return
        self.email_verified = True
        self.save(
            update_fields=[
                "email_verified",
            ]
        )

    def verify_mobile(self):
        if self.mobile_verified:
            return
        self.mobile_verified = True
        self.save(update_fields=["mobile_verified"])

    def reset_password(self, raw_password):
        super().set_password(raw_password)
        self.last_password_change_at = timezone.now()
        self.save(
            update_fields=[
                "password",
                "last_password_change_at",
            ]
        )

    def get_org_member(self, org):
        """
        Returns a `OrganizationMember` instance
        """
        from soteria.models import Organization
        from soteria.orgs.models import OrganizationMember

        organization: Organization = org

        try:
            return OrganizationMember.objects.get(user=self, organization=organization)
        except OrganizationMember.DoesNotExist:
            return None
