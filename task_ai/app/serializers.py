from rest_framework import serializers
from task_ai.app.models import (
    Task,
    CustomUser,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True, view_name="task-detail", read_only=True
    )

    class Meta:
        model = CustomUser
        fields = ["url", "username", "email", "tasks", "thread_id"]


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

    class Meta:
        model = Task
        fields = ["url", "user", "title", "description", "completed"]
