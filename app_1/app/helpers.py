from django.core.mail import send_mail
from django.conf import settings 


def send_forgot_password_mail(email , token ):
    subject = 'Your forgot password link'
    message = f'Hi , click on the link to reset your password http://radiocinema.parastechnologies.in/change/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
