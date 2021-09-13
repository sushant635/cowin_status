from celery import shared_task
# from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from cowin_status_app import settings
from django.utils import timezone
from datetime import timedelta


@shared_task(bind=True)
def send_mail_func(self,email,message):
    to_email = email
    message = message
    mail_subject = 'Hi! Username and Password'

    send_mail(
        subject = mail_subject,
        message = message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return 'Done'