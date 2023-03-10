from django.core.exceptions import ImproperlyConfigured


class InvalidSMSBackendError(ImproperlyConfigured):
    pass


class BaseSMSBackendError(Exception):
    pass


class SMSBackendError(BaseSMSBackendError):
    pass


class SendSMSError(BaseSMSBackendError):
    pass


class InvalidOTPError(BaseSMSBackendError):
    pass
