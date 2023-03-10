import logging

from django.core.exceptions import ImproperlyConfigured

from soteria.sms.backends.base import BaseSMSBackend
from soteria.utils.email import send_email
from soteria.utils.otp import save_otp, verify_otp

logger = logging.getLogger()


class EmailBased(BaseSMSBackend):
    OTP_NAMESPACE = "sms_backend_emailbased_otp"

    def __init__(self, params):
        super().__init__(params)

        self.email_to = self.get_option("EMAIL_TO")
        if not self.email_to:
            raise ImproperlyConfigured("'EMAIL_TO' is required to use email based sms backend")

    def _send_sms(self, mobile_number, text_message, template_id=None):
        subject = f"{mobile_number} received a new SMS"
        self._send_email(subject, text_message)

    def _send_otp(self, mobile_number, text_message, otp, template_id=None):
        otp = otp or self.generate_otp()
        save_otp(
            mobile_number,
            otp=otp,
            expires_in=self.otp_expiry_secs,
            namespace=self.OTP_NAMESPACE,
        )

        subject = f"{mobile_number} received a new OTP"
        self._send_email(subject, text_message)

    def _verify_otp(self, mobile_number, otp):
        if not verify_otp(mobile_number, otp, namespace=self.OTP_NAMESPACE):
            raise self.raise_invalid_otp("Incorrect or expired OTP")

    def _send_email(self, subject, text_body):
        send_email(
            self.email_to,
            subject,
            text_body=text_body,
        )
