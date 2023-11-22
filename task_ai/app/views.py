from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions, viewsets
from task_ai.app.handlers import (
    post_prompt_handler,
    get_prompt_handler,
)
from task_ai.app.models import (
    Task,
    Instruction,
    CustomUser as User,
)
from task_ai.app.serializers import (
    UserSerializer,
    TaskSerializer,
    InstructionSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InstructionViewSet(viewsets.ModelViewSet):
    queryset = Instruction.objects.all().order_by("-created_at")
    serializer_class = InstructionSerializer


class PromptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return post_prompt_handler(request)

    def get(self, request):
        return get_prompt_handler(request)


@api_view(["GET"])
def get_status(request):
    return get_prompt_handler(request)
