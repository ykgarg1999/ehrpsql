from django.core.mail import send_mail
from django.conf import settings

class Util:
    @staticmethod
    def sent_email(data, email):
        send_mail(data['email_subject'], data['email_body'], settings.EMAIL_HOST_USER, [email])
