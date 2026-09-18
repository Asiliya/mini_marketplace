import os

from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "newdjango.settings",
)

app = Celery("newdjango")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "cleanup-expired-tokens": {
        "task": "user.tasks.cleanup_expired_tokens",
        "schedule": 300.0,
    },
}