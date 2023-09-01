from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet, basename='complaint')

urlpatterns = [
    path('', include(router.urls)),
    path('complaintuser/<int:employee_id>/', views.user_complaint_list, name='user_complaint_list'),
   
]