from django.urls import path

from soteria.auth.views.email_signin import UserEmailSigninAPI
from soteria.auth.views.email_verify import (
    EmailVerificationReSendOTPAPI,
    EmailVerificationSendOTPAPI,
    EmailVerificationVerifyOTPAPI,
)
from soteria.auth.views.forget_password import ForgotPasswordAPI
from soteria.auth.views.mobile_signin import UserMobileSigninAPI, UserMobileSigninSendOTPAPI
from soteria.auth.views.mobile_verify import (
    MobileVerificationAPI,
    MobileVerificationReSendOTPAPI,
    MobileVerificationSendOTPAPI,
)
from soteria.auth.views.refresh_token import RefreshAccessTokenAPI
from soteria.auth.views.reset_password import ResetPasswordAPI
from soteria.auth.views.user_signup import UserSignupAPI

urlpatterns = [
    path("api/v1/auth/signup/", UserSignupAPI.as_view(), name="user-signup"),
    path(
        "api/v1/auth/login/mobile/send-otp/",
        UserMobileSigninSendOTPAPI.as_view(),
        name="user-send-login-otp",
    ),
    path("api/v1/auth/login/mobile/", UserMobileSigninAPI.as_view(), name="user-mobile-login"),
    path("api/v1/auth/login/email/", UserEmailSigninAPI.as_view(), name="user-email-login"),
    path(
        "api/v1/auth/email-verification/send-otp/",
        EmailVerificationSendOTPAPI.as_view(),
        name="auth-email-verify-send-otp",
    ),
    path(
        "api/v1/auth/email-verification/resend-otp/",
        EmailVerificationReSendOTPAPI.as_view(),
        name="auth-email-verify-resend-otp",
    ),
    path(
        "api/v1/auth/email-verification/",
        EmailVerificationVerifyOTPAPI.as_view(),
        name="auth-email-verify",
    ),
    path(
        "api/v1/auth/mobile-verification/resend-otp/",
        MobileVerificationReSendOTPAPI.as_view(),
        name="auth-mobile-verify-resend-otp",
    ),
    path(
        "api/v1/auth/mobile-verification/send-otp/",
        MobileVerificationSendOTPAPI.as_view(),
        name="auth-mobile-verify-send-otp",
    ),
    path(
        "api/v1/auth/mobile-verification/",
        MobileVerificationAPI.as_view(),
        name="auth-mobile-verify",
    ),
    path("api/v1/auth/forgot-password/", ForgotPasswordAPI.as_view(), name="auth-forgot-password"),
    path("api/v1/auth/reset-password/", ResetPasswordAPI.as_view(), name="auth-reset-password"),
    path("api/v1/auth/token/refresh/", RefreshAccessTokenAPI.as_view(), name="auth-token-refresh"),
]
