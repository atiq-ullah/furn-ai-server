from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework import permissions
from task_ai.app import views

SchemaView = get_schema_view(
    openapi.Info(
        title="TaskAI API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"tasks", views.TaskViewSet)
router.register(r"instructions", views.InstructionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("admin", admin.site.urls),
    path("prompt", views.PromptView.as_view(), name="prompt"),
    path("status", views.get_status, name="status"),

    # Swagger
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),

    path(
        "swagger/",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
