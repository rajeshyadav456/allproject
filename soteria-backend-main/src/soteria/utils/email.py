from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def send_email(
    to_email,
    subject,
    text_body=None,
    html_body=None,
    attachments=None,
    alternatives=None,
    from_email=None,
):
    if not text_body and not html_body:
        raise Exception("'text_body' or 'html_body' is missing")

    if isinstance(to_email, str):
        to_email = [to_email]

    text_body = strip_tags(html_body) if html_body else text_body
    alternatives = alternatives or []
    if html_body:
        alternatives.append((html_body, "text/html"))
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to_email,
        attachments=attachments,
        alternatives=alternatives,
    )
    email.send()
