import time
from dotenv import load_dotenv

load_dotenv()

from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

celery = Celery("handlers", broker="pyamqp://", backend="rpc://")
