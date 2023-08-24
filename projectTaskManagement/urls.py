from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("", include(router.urls)),
    path("individualtasks/<int:pk>/", individual_task, name="individual-task"),
    path("usertasks/<int:pk>/", update_task_status, name="update-task-status"),
]
