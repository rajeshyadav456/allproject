import logging
from typing import List
from urllib.parse import urlencode

from django.core.exceptions import ImproperlyConfigured

from soteria.sms.backends.base import BaseSMSBackend
from soteria.utils.http import request_with_retry
from soteria.utils.otp import save_otp, verify_otp

logger = logging.getLogger(__name__)


class AirtelApiClient:
    base_url = "http://digimate.airtel.in:15181"

    def __init__(
        self,
        username,
        password,
        sender_id,
        params,
    ):
        self.username = username
        self.password = password
        self.sender_id = sender_id
        self.params = params

    def append_query_params_to_url(self, url, query_params):
        query_params_str = (
            urlencode(query_params) if isinstance(query_params, dict) else query_params
        )
        if "?" not in url:
            url += "?"

        if "?" in url and not url.endswith("?"):
            url += "&"

        if query_params_str:
            url += query_params_str

        return url

    def call_send_sms(self, mobile_numbers: List, content, template_id):
        """
        Send Request to Send SMS .
        :mobile_numbers : numbers of receptions.
        :Single SMS ["+9199999999"]
        :Bulk SMS ["+9199999999","+9188888888"]

        :NOTE: Add support for sms_template_id:

        """
        if not template_id:
            raise ImproperlyConfigured("Template id is missing.")
        query_params = {
            "loginID": self.username,
            "password": self.password,
            "mobile": mobile_numbers,
            "text": content,
            "senderid": self.sender_id,
            "DLT_TM_ID": template_id,
            "DLT_CT_ID": self.params["AIRTEL_DLT_CT_ID"],
            "DLT_PE_ID": self.params["AIRTEL_DLT_PE_ID"],
            "route_id": self.params["AIRTEL_ROUTE_ID"],
            "Unicode": self.params["AIRTEL_UNICODE"],
            "camp_name": self.params["AIRTEL_CAMP_NAME"],
        }
        base_url = f"{self.base_url}/BULK_API/SendMessage"
        url = self.append_query_params_to_url(url=base_url, query_params=query_params)
        res = request_with_retry(
            "GET",
            url,
        )
        return res


class Airtel(BaseSMSBackend):
    OTP_NAMESPACE = "sms_backend_airtel"

    def __init__(self, params):
        super().__init__(params)

        username = self.get_option("AIRTEL_LOGIN_ID")
        password = self.get_option("AIRTEL_PASSWORD")
        sender_id = self.get_option("AIRTEL_SENDER_ID")
        params = self._options
        if not username or not password:
            raise ImproperlyConfigured("Airtel Login ID or Password is missing.")
        self.client = AirtelApiClient(
            username=username, password=password, sender_id=sender_id, params=params
        )

    def _send_sms(self, mobile_number, text_message, template_id):
        res = self.client.call_send_sms(mobile_number, text_message, template_id)
        logger.info(f"Response from Airtel send_sms : {res.text}")
        if res.status_code != 200 or res.text != "SUCCESS\n":
            self.raise_error(f"Fail to send sms, got status={res.status_code} : {res.text}")

    def _send_otp(self, mobile_number, text_message, otp, template_id):
        otp = otp or self.generate_otp()
        save_otp(
            mobile_number,
            otp=otp,
            expires_in=self.otp_expiry_secs,
            namespace=self.OTP_NAMESPACE,
        )
        res = self.client.call_send_sms(mobile_number, text_message, template_id)
        logger.info(f"Response from Airtel send_sms : {res.text}")
        if res.status_code != 200 or res.text != "SUCCESS\n":
            self.raise_error(f"Fail to send sms, got status={res.status_code} : {res.text}")

    def _verify_otp(self, mobile_number, otp):
        if not verify_otp(mobile_number, otp, namespace=self.OTP_NAMESPACE):
            raise self.raise_invalid_otp("Incorrect or expired OTP")
