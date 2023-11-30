from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from task_ai.signals import MQ_ADDRESS, MQ_PORT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_ai.settings")


MQ_ADDRESS = os.environ.get("MQ_ADDRESS", "localhost")
MQ_PORT = os.environ.get("MQ_PORT", 5672)
BROKER = f"amqp://{MQ_ADDRESS}:{MQ_PORT}"

app = Celery("task_ai", broker=BROKER)  # type: ignore
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
