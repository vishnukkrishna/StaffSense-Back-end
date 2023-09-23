from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MeetingViewSet


router = DefaultRouter()
router.register(r"meetings", MeetingViewSet)

urlpatterns = [
    path("meeting/", include(router.urls)),
]
