import time
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

celery = Celery('handlers.handlers', broker='pyamqp://', backend='rpc://')