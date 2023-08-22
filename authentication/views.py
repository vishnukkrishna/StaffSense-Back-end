from django.shortcuts import render
from rest_framework.views import APIView
from authentication.serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import *
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from rest_framework.decorators import api_view
from jwt.exceptions import InvalidTokenError
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser

# Create your views here.


class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = Employee.objects.get(email=email)
        print(user, "userrrrrrrrr")
        if user is None:
            return Response(
                {"error": "No such admin exist"}, status=status.HTTP_400_BAD_REQUEST
            )
            # raise AuthenticationFailed("No such admin exist")
        if not user.check_password(password):
            print("pass")
            return Response(
                {"error": "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST
            )
            # raise AuthenticationFailed("Incorrect Password")
        if not user.is_superuser:
            return Response(
                {"error": "No admin privileges"}, status=status.HTTP_400_BAD_REQUEST
            )
            # raise AuthenticationFailed("No admin privileges")
        access_token = AccessToken.for_user(user)
        access_token["name"] = "Admin"
        access_token["email"] = user.email
        access_token["is_active"] = user.is_active

        access_token["is_admin"] = user.is_superuser
        access_token = str(access_token)

        return Response(
            {
                "access_token": access_token,
            }
        )


def Employeedetails(request, user_id):
    try:
        user = Employee.objects.get(id=user_id)
        serializer = UserDataSerializer(user)
        return JsonResponse(serializer.data)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)


class EmployeeRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        email = validated_data.get("email")
        username = validated_data.get("username")
        department = validated_data.get("department")

        temporary_password = validated_data.get("temporaryPassword")

        department = Department.objects.get(name=department)

        employee = Employee.objects.create(
            email=email,
            username=username,
            department=department,
            password=make_password(temporary_password),
        )

        # Generate and store the email verification token
        email_token = default_token_generator.make_token(employee)
        employee.email_token = email_token
        employee.save()

        tokens = generate_tokens(employee)

        accessToken = tokens["access"]

        send_email_to_employee(
            email, username, employee.id, temporary_password, accessToken
        )
        # send_email_to_employee(email,username, employee.id, temporary_password, email_token)

        print("successs", department)
        response_data = {
            "message": "Employee registered successfully.",
            "username": username,
            "email": email,
            "department": department.name,
            "temporaryPassword": temporary_password,
            "tokens": tokens,
        }

        return Response(response_data, status=status.HTTP_200_OK)


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    # Return both refresh and access tokens
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def send_email_to_employee(email, username, user_id, temporary_password, email_token):
    # verification_link = f'http://localhost:3000/user?token={email_token}'
    verification_link = (
        f"http://localhost:3000/user?token={email_token}&user_id={user_id}"
    )

    subject = "Welcome to Our Company"
    message = f"Dear employee, your account has been created. username is {username} and password is {temporary_password } Please verify your email using the following link:\n\n{verification_link}\n\nThank you!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@api_view(["POST"])
def verify_token(request):
    token = request.data["token"]

    SECRET_KEY = "django-insecure-q&j^&vzefm_+0dhxl(zgunz!w%7v-51$a_w1uzav5y3%e0efe_"
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Token is valid

        user_id = decoded_token["user_id"]

        employee = Employee.objects.get(id=user_id)
        if employee.email_token:
            # Mark the token as expired or delete it from the Employee model
            employee.email_token = (
                ""  # Mark the token as expired (set it to an empty string)
            )
            employee.save()

            jwt_token = jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")
            return Response({"valid": True, "jwt_token": jwt_token, "status": 200})

        else:
            return Response({"valid": True, "jwt_token": "", "status": 404})

        # Generate JWT token
    except InvalidTokenError as e:
        return Response({"valid": False}, status=400)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print("reched backendddddddddddddddddddddd")
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            print("here")
            # Authentication successful, generate a new JWT token
            data = request.data
            print(data)
            email = data["email"]
            print(email,"emailllllllllll")
            # user =  Employee.objects.get(email=email)
            employee = Employee.objects.select_related("department").get(email=email)
            print(employee,"jjjjjjj")
            department_name = employee.department.name
            print("here")
            print(employee, "im the bosssss")
            print(department_name, "department is ourssssssss")
            # user_id = user.id

            print(employee.first_name + " " + employee.last_name, "heyy")
            payload = {
                "name": employee.first_name + " " + employee.last_name,
                "username": employee.username,
                "user_id": employee.id,
                "email": email,
                "is_active": employee.is_active,
                "is_blocked": employee.is_blocked,
                "designation": employee.designation,
                "department": department_name,
                "is_admin": employee.is_superuser,
                "exp": datetime.utcnow() + timedelta(minutes=15),
            }

            print(payload, "hello payload")
            access_token = jwt.encode(
                payload, settings.SECRET_KEY, algorithm="HS256"
            ).decode("utf-8")

            print(access_token, "accesssssss tokennnnnnnn")
            return Response({"access_token": access_token})

        else:
            # Authentication failed
            print("erooorrrrrrrrrrrrrrrrrrrrrrrr")
            return response
