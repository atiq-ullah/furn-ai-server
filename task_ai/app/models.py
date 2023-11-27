from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    thread_id = models.IntegerField(default=-1)


class Task(models.Model):
    user = models.ForeignKey(CustomUser, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
