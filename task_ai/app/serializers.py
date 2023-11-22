from rest_framework import serializers
from task_ai.app.models import (
    Task,
    Instruction,
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


class InstructionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instruction
        fields = ["url", "content", "created_at", "instruction_type"]
