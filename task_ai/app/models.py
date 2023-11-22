from django.db import models
from django.contrib.auth.models import AbstractUser

MAX_INSTRUCTION_LENGTH = 32768


class CustomUser(AbstractUser):
    thread_id = models.IntegerField(default=-1)


class Task(models.Model):
    user = models.ForeignKey(CustomUser, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)


class Instruction(models.Model):
    content = models.CharField(max_length=MAX_INSTRUCTION_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    instruction_type = models.CharField(max_length=20)
