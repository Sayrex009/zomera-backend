import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(length=6):
    return str(random.randint(10**(length-1), 10**length - 1))

def send_otp_email(email, otp):
    subject = "Ваш код подтверждения"
    message = f"Ваш OTP код: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
