from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login"),
    path("userdetails/<int:user_id>/", Employeedetails, name="userdetails"),
    path("registration/", EmployeeRegistrationView.as_view(), name="registration/"),
    path("verify-token/", verify_token, name="verify_token"),
    path("userlogin/", LoginView.as_view(), name="login"),
    path("employelist/", EmployeeListView.as_view(), name="employelist"),
    path(
        "blockemployees/<int:employee_id>/",
        BlockEmployeeView.as_view(),
        name="block_employee",
    ),
    path(
        "unblockemployees/<int:employee_id>/",
        UnblockEmployeeView.as_view(),
        name="unblock_employee",
    ),
    path("edit/<int:pk>/", EmployeeEditView.as_view(), name="employeee-detail"),
    path("details/<int:pk>/", EmployeeEditView.as_view(), name="details"),
    path("departments/", DepartmentListAPIView.as_view(), name="departments"),
    path(
        "departments/<int:pk>/",
        DepartmentListAPIView.as_view(),
        name="department_detail",
    ),
    path(
        "departments/<int:pk>/",
        DepartmentListAPIView.as_view(),
        name="department-update",
    ),
    path("add_department/", add_department, name="add_department"),
    path("announcements/", AnnouncementEditView.as_view()),
    path(
        "announcements/<int:announcement_id>/delete/",
        AnnouncementEditView.as_view(),
        name="announcement_delete",
    ),
]
