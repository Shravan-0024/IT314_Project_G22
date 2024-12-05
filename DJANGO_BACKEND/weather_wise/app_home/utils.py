from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From email
            recipient_list,  # To email(s)
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False