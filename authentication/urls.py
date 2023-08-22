from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin_login"),
    path("userdetails/<int:user_id>/", Employeedetails, name="userdetails"),
    path("registration/", EmployeeRegistrationView.as_view(), name="registration/"),
    path("verify-token/", verify_token, name="verify_token"),
    path("userlogin/", LoginView.as_view(), name="login"),
]
