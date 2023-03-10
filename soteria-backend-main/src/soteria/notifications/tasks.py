from soteria.sms import default_sms_backend
from soteria.tasks.base import instrumented_task
from soteria.utils.email import send_email


@instrumented_task(name="soteria.notifications.tasks.send_email_task")
def send_email_task(*args, **kwargs):
    send_email(*args, **kwargs)


@instrumented_task(name="soteria.notifications.tasks.send_text_sms_task")
def send_text_sms_task(mobile_number, text_message, template_id=None):
    default_sms_backend.send_sms(mobile_number, text_message, template_id=template_id)


@instrumented_task(name="soteria.notifications.tasks.send_otp_sms_task")
def send_otp_sms_task(mobile_number, text_message, template_id=None):
    default_sms_backend.send_otp(mobile_number, text_message, template_id=template_id)
