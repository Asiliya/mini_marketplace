from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from .models import (
    EmailVerificationToken,
    PasswordResetToken,
)
from .services import (
    send_verification_email,
    send_password_reset_email,
)


@shared_task
def send_verification_email_task(token_id):
    token = EmailVerificationToken.objects.select_related(
        "user"
    ).get(id=token_id)

    send_verification_email(
        token.user,
        token,
    )


@shared_task
def send_password_reset_email_task(token_id):
    token = PasswordResetToken.objects.select_related(
        "user"
    ).get(id=token_id)

    send_password_reset_email(
        token.user,
        token,
    )


@shared_task
def cleanup_expired_tokens():
    now = timezone.now()

    verification_cutoff = now - timedelta(hours=12)

    expired_tokens = (
        EmailVerificationToken.objects
        .filter(
            created_at__lt=verification_cutoff,
            user__is_verified=False,
        )
        .select_related("user")
    )

    for token in expired_tokens:
        user = token.user

        latest_token = (
            EmailVerificationToken.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if latest_token and latest_token.id == token.id:
            user.delete()

    reset_cutoff = now - timedelta(minutes=15)

    PasswordResetToken.objects.filter(
        created_at__lt=reset_cutoff
    ).delete()