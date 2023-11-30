from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, viewsets

from task_ai.openai_client import (
    PromptType,
    add_message_to_thread,
    get_message_list,
    start_run_on_thread,
    validate_request,
)

from task_ai.tasks import (
    monitor_run_status,
)

from task_ai.app.models import (
    Task,
    CustomUser as User,
)
from task_ai.app.serializers import (
    UserSerializer,
    TaskSerializer,
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


class PromptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest):
        validation = validate_request(request)
        if validation is not None:
            return validation
        p_type = PromptType(request.POST.get("p_type"))
        prompt = request.POST.get("prompt")
        if p_type is not None and prompt is not None:
            message_id = add_message_to_thread(p_type, prompt)
            run_id = start_run_on_thread(p_type)
            monitor_run_status.delay(p_type.value, run_id)
            return JsonResponse({"message_id": message_id, "run_id": run_id})
        return JsonResponse({"error": "Invalid prompt or p_type"}, status=400)

    def get(self, request: HttpRequest):
        validation = validate_request(request)
        if validation is not None:
            return validation
        p_type = PromptType(request.GET.get("p_type"))
        if p_type is not None:
            return HttpResponse(get_message_list(p_type))
        return JsonResponse({"error": "Invalid p_type"}, status=400)


def index(request):
    return render(request, "index.html")
