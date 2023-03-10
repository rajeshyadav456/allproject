import logging

from soteria.core.notification import UserMobileSigninOTPNotification

logger = logging.getLogger(__name__)


def send_mobile_signin_otp(mobile_number: str):
    """
    Send signin otp
    """
    notification = UserMobileSigninOTPNotification()
    notification.send_sms(mobile_number)
    logger.info(f"OTP sent for mobile signin to {mobile_number}")


def is_valid_mobile_signin_otp(mobile_number: str, otp: str):
    """
    Verify signin otp
    """
    notification = UserMobileSigninOTPNotification()
    if not notification.verify_otp(mobile_number, otp):
        return False
    return True
