from django.conf import settings

from soteria.core.notification import UserEmailVerifyNotification
from soteria.models import User
from soteria.utils.otp import save_otp, verify_otp

VERIFY_EMAIL_NAMESPACE = "email_verification_otp"


def send_verify_email_otp(user: User):
    """
    Send a new verify email OTP to user email
    """
    email = user.email
    otp_expiry_time = settings.DEFAULT_SMS_OTP_EXPIRY_SEC
    otp = save_otp(key=email, expires_in=otp_expiry_time, namespace=VERIFY_EMAIL_NAMESPACE)

    notification = UserEmailVerifyNotification()
    notification.send_email_async(
        email,
        context={
            "otp": otp,
            "user_email": email,
            "otp_expires_in_mins": otp_expiry_time // 60,
        },
    )


def is_valid_email_verify_otp(user: User, otp: str):
    """
    Checks whether given otp is valid for this user to verify email
    """
    email = user.email
    if not verify_otp(key=email, otp=otp, namespace=VERIFY_EMAIL_NAMESPACE):
        return False
    return True
