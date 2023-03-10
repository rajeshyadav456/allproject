import logging

import jwt
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

from soteria.sms.backends.base import BaseSMSBackend
from soteria.utils import to_cs_str
from soteria.utils.datetime_util import epoch_to_dt, get_current_datetime
from soteria.utils.http import request_with_retry
from soteria.utils.otp import save_otp, verify_otp

logger = logging.getLogger(__name__)


class ValueFirstApiClient:
    base_url = "https://http.myvfirst.com"
    AUTH_TOKEN_CACHE_KEY = "valuefirst_auth_token"  # nosec: B105

    def __init__(
        self,
        username,
        password,
        sender_id,
        timeout=None,
        auth_token=None,
    ):
        self.username = username
        self.password = password
        self.sender_id = sender_id
        self.timeout = timeout
        self._auth_token = None

        cached_auth_token = cache.get(key=self.AUTH_TOKEN_CACHE_KEY)
        if not auth_token:
            auth_token = cached_auth_token

        if auth_token:
            self.store_auth_token(auth_token)

    @staticmethod
    def get_token_expires_at(jwt_token):
        payload = jwt.decode(jwt_token, options={"verify_signature": False})
        exp_at = payload["exp"]
        expires_at = epoch_to_dt(exp_at)
        return expires_at

    @staticmethod
    def is_auth_token_expired(auth_token, expire_in=3600):
        """
        Checks whether an auth token is expired or going to expire in given
        time.
        """
        if not auth_token:
            return True

        token_expires_at = ValueFirstApiClient.get_token_expires_at(auth_token)
        now = get_current_datetime()

        # token is already expired
        if now > token_expires_at:
            return True

        # token is still valid and not expired yet, but going to expire soon
        diff_seconds = (now - token_expires_at).total_seconds()
        if now < token_expires_at and diff_seconds > expire_in:
            return True

        return False

    def refresh_token(self):
        new_auth_token = self.generate_token()
        self.store_auth_token(new_auth_token)

    def store_auth_token(self, auth_token):
        self._auth_token = auth_token
        cache.set(key=self.AUTH_TOKEN_CACHE_KEY, value=auth_token, timeout=None)

    def get_auth_token(self):
        if self.is_auth_token_expired(self._auth_token):
            self.refresh_token()
        return self._auth_token

    def generate_token(self):
        params = {"action": "generate"}
        url = f"{self.base_url}/smpp/api/sendsms/token"
        res = request_with_retry(
            "POST",
            url,
            params=params,
            timeout=self.timeout,
            auth=(self.username, self.password),
        )
        token = res.json()["token"]
        return token

    def get_send_sms_headers(self):
        return {"Authorization": f"Bearer {self.get_auth_token()}"}

    def call_send_sms(self, mobile_numbers, content):
        params = {
            "from": self.sender_id,
            "text": content,
        }
        if isinstance(mobile_numbers, (list, tuple)):
            mobile_numbers = to_cs_str(mobile_numbers)
            params["to"] = mobile_numbers
            params["category"] = "bulk"
        else:
            params["to"] = mobile_numbers

        url = f"{self.base_url}/smpp/sendsms"
        headers = self.get_send_sms_headers()
        res = request_with_retry(
            "GET",
            url,
            params=params,
            timeout=self.timeout,
            headers=headers,
        )
        return res


class ValueFirst(BaseSMSBackend):
    OTP_NAMESPACE = "sms_backend_valuefirst"

    def __init__(self, params):
        super().__init__(params)

        username = self.get_option("VALUEFIRST_USERNAME")
        password = self.get_option("VALUEFIRST_PASSWORD")
        auth_token = self.get_option("VALUEFIRST_AUTH_TOKEN")
        if not username or not password:
            raise ImproperlyConfigured("username or password is missing in " "valuefirst")
        self.client = ValueFirstApiClient(
            username=username,
            password=password,
            sender_id=self.sender_name,
            timeout=5,
            auth_token=auth_token,
        )

    def _send_sms(self, mobile_number, text_message, template_id=None):
        res = self.client.call_send_sms(mobile_number, text_message)
        logger.info(f"Response from ValueFirst send_sms : {res.text}")
        if res.status_code != 200 or res.text != "Sent.":
            self.raise_error(f"Fail to send sms, got status={res.status_code} : {res.text}")

    def _send_otp(self, mobile_number, text_message, otp, template_id=None):
        otp = otp or self.generate_otp()
        save_otp(
            mobile_number,
            otp=otp,
            expires_in=self.otp_expiry_secs,
            namespace=self.OTP_NAMESPACE,
        )
        res = self.client.call_send_sms(mobile_number, text_message)
        logger.info(f"Response from ValueFirst send_sms : {res.text}")
        if res.status_code != 200 or res.text != "Sent.":
            self.raise_error(f"Fail to send sms, got status={res.status_code} : {res.text}")

    def _verify_otp(self, mobile_number, otp):
        if not verify_otp(mobile_number, otp, namespace=self.OTP_NAMESPACE):
            raise self.raise_invalid_otp("Incorrect or expired OTP")
