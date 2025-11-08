# app/celery_app.py
import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RESULT_URL = os.getenv("RESULT_URL", "redis://localhost:6379/1")

celery = Celery(
    "email_worker",
    broker=REDIS_URL,
    backend=RESULT_URL,
    include=["app.tasks.email_tasks"],   
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_acks_on_failure_or_timeout=True,
    broker_transport_options={"visibility_timeout": 3600},
)

celery.conf.beat_schedule = {
    "send-weekly-digest": {
        "task": "app.tasks.email_tasks.send_weekly_digest",
        "schedule": crontab(hour=10, minute=0, day_of_week="sun"),
    }
}
