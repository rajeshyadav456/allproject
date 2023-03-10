from soteria.notifications.base import BaseNotification, BaseOTPNotification


class UserEmailVerifyNotification(BaseNotification):
    email_subject_template = "[Soteria] Email Verification"
    email_html_template_path = "auth/user_email_verify.txt"


class UserResetPasswordNotification(BaseNotification):
    email_subject_template = "[Soteria] Reset your account password"
    email_html_template_path = "auth/reset_password.txt"


class MobileVerificationOTPNotification(BaseOTPNotification):
    sms_template = "Your Soteria One Time Password (OTP) is %OTP% . The OTP is confidential and should not be shared with anyone."
    sms_template_id = "1001096933494158"


class UserMobileSigninOTPNotification(BaseOTPNotification):
    sms_template = "Your Soteria One Time Password (OTP) is %OTP% . The OTP is confidential and should not be shared with anyone."
    sms_template_id = "1001096933494158"


class OrganizationNewMemberNotification(BaseNotification):
    email_subject_template = "[Soteria] To Join {organization.name}"
    email_html_template_path = "orgs/new_org_member_invite.txt"


class OrganizationExistingMemberNotification(BaseNotification):
    email_subject_template = "[Soteria] To Join {organization.name}"
    email_html_template_path = "orgs/existing_org_member_invite.txt"
