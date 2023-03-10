import rest_framework.fields
from django.conf import settings
from django.contrib.auth.password_validation import (
    ValidationError,
    get_password_validators,
    validate_password,
)
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import DjangoValidationError, get_error_detail
from timezone_field import rest_framework as tz_fields

from soteria.utils.mobile_number import (
    CallingCodeInvalid,
    CallingCodeNotSupported,
    MobileNumberLengthInvalid,
    format_mobile_number,
    is_valid_mobile_number,
)


class MobileNumberField(serializers.CharField):
    """
    A mobile number field for doing format validation and also do calling
    code support check for system and return international formatted mobile
    number
    """

    default_error_messages = {
        "invalid_mobile_number": _("Not a valid mobile number."),
        "invalid_calling_code": _("Not a valid calling code in mobile number"),
        "system_not_support_calling_code": _(
            "Calling code {calling_code} is not supported by system"
        ),
        "invalid_mobile_number_length": _("Mobile number length is invalid"),
    }

    def __init__(self, **kwargs):
        self.cc_support_check = kwargs.pop("cc_support_check", True)
        super().__init__(**kwargs)

    def get_default_calling_code(self):
        return settings.DEFAULT_CALLING_CODE

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        default_calling_code = self.get_default_calling_code()
        cc_support_check = self.cc_support_check
        try:
            if not is_valid_mobile_number(
                mobile_number=data,
                calling_code=default_calling_code,
                cc_support_check=cc_support_check,
            ):
                self.fail("invalid_mobile_number")
        except MobileNumberLengthInvalid:
            self.fail("invalid_mobile_number_length")
        except CallingCodeInvalid:
            self.fail("invalid_calling_code")
        except CallingCodeNotSupported as e:
            # hack to do pass exception message as validation error message
            # for this key
            self.error_messages["system_not_supported_calling_code"] = str(e)

            self.fail("system_not_supported_calling_code")

        # Now we are sure that we have data which is mobile number with valid
        # format and calling code
        mobile_number = format_mobile_number(data, calling_code=default_calling_code)

        return mobile_number


class PasswordSerializersField(rest_framework.fields.CharField):
    MIN_LENGTH = 8
    MAX_LENGTH = 50

    def __init__(self, disable_validate_password=False, **kwargs):
        # min length validation will be managed by django validator
        kwargs["max_length"] = PasswordSerializersField.MAX_LENGTH
        kwargs["allow_blank"] = False
        kwargs["trim_whitespace"] = False
        super().__init__(**kwargs)
        self._django_validators = self.get_django_validators()

        # This will control the validation process of password related to
        # it's strength which we mostly do using django validators. If set
        # True, field will do necessary field label validations but not do
        # django password validation
        self.disable_validate_password = disable_validate_password

    def get_django_validators(self):
        validator_config = [
            {
                "NAME": "django.contrib.auth.password_validation"
                ".UserAttributeSimilarityValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation" ".MinimumLengthValidator",
                "OPTIONS": {"min_length": PasswordSerializersField.MIN_LENGTH},
            },
            {
                "NAME": "django.contrib.auth.password_validation" ".CommonPasswordValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation" ".NumericPasswordValidator",
            },
        ]
        return get_password_validators(validator_config)

    def run_validators(self, value):
        # first run DRF serializer field validators
        super().run_validators(value)

        if self.disable_validate_password:
            return

        # then, do django based password validation
        try:
            user = self.context.get("user")
            validate_password(value, user=user, password_validators=self._django_validators)
        except DjangoValidationError as exc:
            raise ValidationError(get_error_detail(exc))


class EmailSerializerField(rest_framework.fields.EmailField):
    def __init__(self, **kwargs):
        # https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address
        kwargs["max_length"] = 256

        # by default, we want this setting enabled,
        self.to_lower = kwargs.pop("to_lower", True)

        super().__init__(**kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return value.lower() if self.to_lower else value


class TimeZoneSerializerField(tz_fields.TimeZoneSerializerField):
    def to_internal_value(self, data):
        # CAUTION: This check we are doing because base class
        # implementation will raise ValueError for blank data
        # ValueError: ZoneInfo keys must be normalized relative paths, got:
        if not data:
            self.fail("invalid")
        return super().to_internal_value(data)
