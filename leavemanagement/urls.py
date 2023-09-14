from django.urls import path
from . import views
from .views import *

# from django.contrib.auth import views as auth_views

urlpatterns = [
    path("leaves/", LeaveApplicationView.as_view(), name="leave-application"),
    path(
        "userleave/<int:employee_id>/",
        UserLeaveDataView.as_view(),
        name="user-leave-data",
    ),
    path("employee_leave_requests/<int:employee_id>/", get_employee_leave_requests),
    path(
        "dashboard_data/", views.DashboardDataAPIView.as_view(), name="dashboard_data"
    ),
]
