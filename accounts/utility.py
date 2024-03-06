import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

email_regex = re.compile(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+")
username_regex = re.compile(r"^[a-z0-9_-]{3,15}$")


def check_email(email):
    if re.fullmatch(email_regex, email):
        email = 'email'
    else:
        data = {
            "success": False,
            "message": "Email noto'g'ri."
        }
        raise ValidationError(data)

    return email


def check_user_type(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input = "email"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        data = {
            "message": "Email yoki username noto'g'ri."
        }
        raise ValidationError(data)
    return user_input


def send_email(email, code):
    subject = "Saytimizga xush kelibsiz!"
    data = {
        "code": code
    }
    msg_html = render_to_string("auth/email_confirm.html", context=data)
    message = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    message.attach_alternative(msg_html, "text/html")
    message.send(fail_silently=False)
