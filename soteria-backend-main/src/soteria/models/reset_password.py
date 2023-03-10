from datetime import timedelta

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip

from soteria.db.models.base import DefaultFieldsModel
from soteria.db.models.utils import sane_repr, sane_str
from soteria.models import User
from soteria.utils import build_url


class ResetPasswordTicketManager(models.Manager):
    def create_ticket(self, user, request):
        now = timezone.now()
        ticket = self.create(
            token=default_token_generator.make_token(user),
            expires_at=now + timedelta(seconds=settings.RESET_PASSWORD_URL_TIMEOUT_SECS),
            client_ip=get_client_ip(request)[0],
            client_ua=request.META["HTTP_USER_AGENT"] or None,
            user=user,
        )
        return ticket


class ResetPasswordTicket(DefaultFieldsModel):
    token = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("token"),
    )
    expires_at = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_("expires at"),
    )
    client_ip = models.CharField(
        max_length=50,
        help_text=_("IP address of the request client."),
        null=True,
        blank=True,
        verbose_name=_("client ip"),
    )
    client_ua = models.CharField(
        max_length=500,
        help_text=_("User agent of client from request."),
        null=True,
        blank=True,
        verbose_name=_("client ua"),
    )
    user = models.ForeignKey(
        "soteria.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("user")
    )

    class Meta:
        app_label = "soteria"
        db_table = "soteria_reset_password"
        verbose_name = _("reset password")
        verbose_name_plural = _("reset passwords")

    __repr__ = sane_repr("id", "user")
    __str__ = sane_str("id", "user")

    objects = ResetPasswordTicketManager()

    @property
    def token_expired(self):
        if self.expires_at > timezone.now():
            return False
        return True

    def set_metadata(self, request):
        self.client_ip = (get_client_ip(request)[0],)
        self.client_ua = request.META["HTTP_USER_AGENT"] or None
        self.save(update_fields=["client_ip", "client_ua"])

    def reset_token(self):
        """
        set attributes to None
        :token
        :expires_at
        """
        self.token = None
        self.expires_at = None
        self.save(update_fields=["token", "expires_at"])

    def is_valid_token(self, user, token):
        """
        Validate token is expired or not
        : True or False
        """
        return default_token_generator.check_token(user, token) and not self.token_expired

    def set_token(self):
        """
        Set reset password token for user
        """
        self.token = default_token_generator.make_token(self.user)
        self.save(update_fields=["token"])

    def set_expires_at(self):
        """
        Set token expiry time
        """
        now = timezone.now()
        self.expires_at = now + timedelta(seconds=settings.RESET_PASSWORD_URL_TIMEOUT_SECS)
        self.save(update_fields=["expires_at"])

    def get_reset_password_link(self, email):
        """
        Return absoule url with query param to reset password
        : {domain}?token=1EFR23RT&email=jhon.doe@email.com
        """
        if not self.token:
            return None
        return build_url(
            settings.RESET_PASSWORD_URL,
            query_params={"token": self.token, "email": email},
        )

    def send_reset_password_notification(self, send=True):
        """
        Send notification to user
        """
        user = self.user
        context = {
            "user": user.email,
            "password_reset_url": self.get_reset_password_link(user.email),
            # seconds to hours conversion
            "url_expiry_hours": int(settings.RESET_PASSWORD_URL_TIMEOUT_SECS / (60 * 60)),
        }
        # Importing here to avoid circular import error
        from soteria.core.notification import UserResetPasswordNotification

        notification = UserResetPasswordNotification()
        if send:
            notification.send_email_async(user.email, context=context)

    def generate_ticket(self, user: User, request):
        self.set_token()
        self.set_expires_at()
        self.set_metadata(request)
        self.user = user
        self.save(update_fields=["user"])

    def regenerate_ticket_and_send_notification(self, user: User, request):
        self.generate_ticket(user, request)
        self.send_reset_password_notification()
