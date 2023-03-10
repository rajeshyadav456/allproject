import logging

from soteria.core.notification import MobileVerificationOTPNotification
from soteria.models import User

logger = logging.getLogger(__name__)


def send_mobile_verify_otp(user: User, mobile_number: str):
    """
    Send OTP to mobile for verification
    """
    notification = MobileVerificationOTPNotification()
    notification.send_sms(mobile_number)
    logger.info(f"OTP sent for mobile verification to {mobile_number}")


def is_valid_mobile_verify_otp(mobile_number: str, otp: str):
    """
    Verify the given OTP and update user's mobile number if OTP is correct
    """
    notification = MobileVerificationOTPNotification()
    if not notification.verify_otp(mobile_number, otp):
        return False
    logger.info(f"OTP successfully verified for mobile number {mobile_number}")
    return True
