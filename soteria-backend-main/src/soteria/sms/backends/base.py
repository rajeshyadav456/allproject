import logging
import re

from django.conf import settings
from django.core.cache import BaseCache, cache
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.sms.constants import MAX_OTP_LENGTH, MIN_OTP_LENGTH
from soteria.sms.exceptions import InvalidOTPError, SMSBackendError
from soteria.utils.mobile_number import (
    CallingCodeNotSupported,
    is_valid_mobile_number,
    split_cc_and_mobile_number,
)
from soteria.utils.otp import generate_otp

logger = logging.getLogger(__name__)

# an otp placeholder which should be present in the content of otp message.
# This will be replaced by client specific otp placeholder
OTP_CODE_PLACEHOLDER_REGEX = re.compile(r"%OTP%")


class BaseSMSBackend:
    # Client specific placeholder for otp code, some clients support OTP
    # generation at their end, only they need a placeholder for replacing it.
    # This setting helps us in configuring that placeholder
    # Please note, OTP message should have `OTP_CODE_PLACEHOLDER_REGEX` in the
    # message, to replace this placeholder.
    # Ex:- if otp_placeholder is XXXX, then otp message would convert to this
    # `%OTP% is your otp` -> `XXXX is your otp`
    otp_placeholder = None

    # .generate_otp() use these characters for otp generation
    otp_chars = "0123456789"

    # a minimum and maximum length of otp this client support
    min_otp_length = MIN_OTP_LENGTH
    max_otp_length = MAX_OTP_LENGTH

    # maximum length of content of SMS is supported. If content length is
    # greater than this, it will raise only warning, but send content
    max_message_length = settings.MAX_MESSAGE_LENGTH

    # list of country calling codes supported by this client.
    cc_supported = settings.ALLOWED_CALLING_CODES

    def __init__(self, params):
        self.sender_name = params.get("SENDER_NAME", settings.DEFAULT_SMS_SENDER_NAME)
        self.max_message_length = params.get("MAX_MESSAGE_LENGTH", settings.MAX_SMS_MESSAGE_LENGTH)
        self.otp_length = params.get("OTP_LENGTH", settings.DEFAULT_SMS_OTP_LENGTH)
        self.otp_expiry_secs = params.get("OTP_EXPIRY_SECS", settings.DEFAULT_SMS_OTP_EXPIRY_SEC)
        self._options = params.get("OPTIONS", {})

    @cached_property
    def _cache(self) -> BaseCache:
        return cache

    def get_option(self, key, default=None):
        return self._options.get(key, default)

    def generate_otp(self):
        return generate_otp(length=self.otp_length, allowed_chars=self.otp_chars)

    def validate_mobile_number(self, mobile_number):
        try:
            if not is_valid_mobile_number(mobile_number):
                raise serializers.ValidationError(_("Invalid mobile number format"))
        except CallingCodeNotSupported as e:
            raise serializers.ValidationError(str(e))

        cc, other = split_cc_and_mobile_number(mobile_number)
        if cc not in self.cc_supported:
            raise serializers.ValidationError(_("Country code '%s' is not supported") % (cc,))
        return mobile_number

    def validate_message_content(self, message):
        max_length = self.max_message_length
        if len(message) >= max_length:
            logger.warning(f"Message exceeded recommended length {max_length}")
        return message

    def validate_otp_length(self, otp_length):
        if otp_length < self.min_otp_length:
            raise serializers.ValidationError(
                f"OTP length can not be less than {self.min_otp_length}"
            )
        if otp_length > self.max_otp_length:
            raise serializers.ValidationError(
                f"OTP length can not be greater than {self.max_otp_length}"
            )
        return otp_length

    def format_mobile_number(self, mobile_number):
        cc, mobile_number = split_cc_and_mobile_number(mobile_number)
        # Currently, we format mobile number by concatenating country
        # calling code as prefix
        return "{cc}{mobile_number}".format(**{"cc": cc, "mobile_number": mobile_number})

    def format_otp_message_content(self, message, otp=None):
        if otp:
            message = OTP_CODE_PLACEHOLDER_REGEX.sub(otp, message)
            return message

        if self.otp_placeholder is None:
            return message

        return OTP_CODE_PLACEHOLDER_REGEX.sub(self.otp_placeholder, message)

    def send_sms(self, mobile_number, text_message, template_id=None):
        mobile_number = self.validate_mobile_number(mobile_number)
        mobile_number = self.format_mobile_number(mobile_number)
        text_message = self.validate_message_content(text_message)
        return self._send_sms(mobile_number, text_message, template_id=template_id)

    def send_otp(self, mobile_number, text_message, template_id=None):
        mobile_number = self.validate_mobile_number(mobile_number)
        mobile_number = self.format_mobile_number(mobile_number)
        otp = self.generate_otp()
        self.validate_otp_length(len(otp))
        text_message = self.format_otp_message_content(text_message, otp)
        text_message = self.validate_message_content(text_message)
        return self._send_otp(mobile_number, text_message, otp, template_id=template_id)

    def resend_otp(self, mobile_number, text_message):
        mobile_number = self.validate_mobile_number(mobile_number)
        mobile_number = self.format_mobile_number(mobile_number)
        otp = self.generate_otp()
        self.validate_otp_length(len(otp))
        text_message = self.format_otp_message_content(text_message, otp)
        text_message = self.validate_message_content(text_message)
        return self._resend_otp(mobile_number, text_message, otp)

    def verify_otp(self, mobile_number, otp):
        mobile_number = self.validate_mobile_number(mobile_number)
        mobile_number = self.format_mobile_number(mobile_number)
        self.validate_otp_length(len(otp))
        return self._verify_otp(mobile_number, otp)

    def _send_sms(self, mobile_number, text_message):
        raise NotImplementedError("subclass of BaseSMSBackend must implement _send_sms()")

    def _send_otp(self, mobile_number, text_message, otp):
        raise NotImplementedError("subclass of BaseSMSBackend must implement _send_otp()")

    def _resend_otp(self, mobile_number, text_message, otp):
        self._send_otp(mobile_number, text_message, otp)

    def _verify_otp(self, mobile_number, otp):
        raise NotImplementedError("subclass of BaseSMSBackend must implement _verify_otp()")

    def raise_error(self, msg, extra=None):
        raise SMSBackendError(msg)

    def raise_invalid_otp(self, msg, extra=None):
        raise InvalidOTPError(msg)
