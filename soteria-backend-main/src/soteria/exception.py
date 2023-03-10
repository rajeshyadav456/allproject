from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed, ValidationError


class InvalidOrganizationConnection(ValidationError):
    default_detail = _("Please set a valid `connection` tenant i.e(Non default tenant).")


class InvalidCredentials(AuthenticationFailed):
    default_detail = _("Invalid credentials")


class AccountAlreadyExists(ValidationError):
    default_detail = _("Account already exists for this user")


class AccountNotFound(ValidationError):
    default_detail = _("No user registered for this account")


class UserEmailUnverified(AuthenticationFailed):
    default_detail = _("Your email address is not verified")


class UserMobileUnverified(AuthenticationFailed):
    default_detail = _("Your mobile number is not verified")
