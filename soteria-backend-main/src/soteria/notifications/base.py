import logging
from typing import Union

from django.template.loader import render_to_string

from soteria.notifications.tasks import send_email_task, send_text_sms_task
from soteria.sms import default_sms_backend
from soteria.sms.exceptions import InvalidOTPError
from soteria.utils.email import send_email

logger = logging.getLogger(__name__)


class BaseNotification:
    sms_template = None
    sms_template_id = None
    email_subject_template = None
    email_html_template_path = None

    def __init__(
        self,
        sms_sender=None,
        context: Union[dict, None] = None,
        **kwargs,
    ):
        self._sms_sender = sms_sender
        self._context = context or {}
        self._kwargs = kwargs

    @property
    def context(self):
        return self._context

    def get_sms_template_id(self):
        return self.sms_template_id

    def get_context(self, context=None):
        if context is not None:
            _context = self.context
            _context.update(**context)
            return _context
        return self.context

    def get_sms_context(self, context=None):
        return self.get_context(context=context)

    def build_sms_message(self, context=None):
        context = self.get_sms_context(context)
        text_message = self.sms_template.format(**context)
        return text_message

    def send_sms(self, mobile_number, context=None):
        template_id = self.get_sms_template_id()
        text_message = self.build_sms_message(context)
        default_sms_backend.send_sms(
            mobile_number=mobile_number, text_message=text_message, template_id=template_id
        )

    def send_sms_async(self, mobile_number, context=None):
        template_id = self.get_sms_template_id()
        text_message = self.build_sms_message(context)
        send_text_sms_task.delay(mobile_number, text_message, template_id=template_id)

    def get_email_context(self, context=None):
        return self.get_context(context=context)

    def build_email_message(self, context=None):
        context = self.get_email_context(context)
        subject = self.email_subject_template.format(**context)
        html_body = render_to_string(
            self.email_html_template_path,
            context,
        )
        return subject, html_body

    def send_email(
        self,
        email,
        context: Union[dict, None] = None,
    ):
        subject, html_body = self.build_email_message(context)
        send_email(email, subject, html_body=html_body)

    def send_email_async(
        self,
        email,
        context: Union[dict, None] = None,
    ):
        subject, html_body = self.build_email_message(context)
        send_email_task.delay(email, subject, html_body=html_body)


class BaseOTPNotification(BaseNotification):
    def send_sms(self, mobile_number, context=None):
        template_id = self.get_sms_template_id()
        text_message = self.build_sms_message(context)
        default_sms_backend.send_otp(
            mobile_number=mobile_number, text_message=text_message, template_id=template_id
        )

    def send_sms_async(self, mobile_number, context=None):
        text_message = self.build_sms_message(context)

        from soteria.notifications.tasks import send_otp_sms_task

        template_id = self.get_sms_template_id()
        send_otp_sms_task.delay_on_commit(mobile_number, text_message, template_id=template_id)

    def verify_otp(self, mobile_number, otp):
        try:
            default_sms_backend.verify_otp(mobile_number, otp)
            return True
        except InvalidOTPError:
            return False
