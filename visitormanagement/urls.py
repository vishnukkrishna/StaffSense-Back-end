from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # path("visitor/", VisitorListAPIView.as_view(), name="visitor"),
    # path(
    #     "visitor/<int:visitor_id>/", VisitorListAPIView.as_view(), name="delete_visitor"
    # ),
    path("visitor/", views.new, name="visitor"),
]
