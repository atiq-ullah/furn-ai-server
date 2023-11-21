from celery import Celery

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task
def add(x, y):
    return x + y
