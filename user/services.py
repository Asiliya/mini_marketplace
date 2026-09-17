from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(user, token):
    verification_url = (
        f"http://127.0.0.1:8000/verify-email/{token.token}/"
    )

    send_mail(
        subject="Verify your email",
        message=(
            f"Hello {user.username}!\n\n"
            f"Click the link to verify your email:\n"
            f"{verification_url}\n\n"
            f"The link is valid for 12 hours."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )