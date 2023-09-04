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
from rest_framework.generics import (
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.filters import SearchFilter

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
        print(user, "yyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        serializer = UserDataSerializer(user)
        print(serializer, "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
        return JsonResponse(serializer.data)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)


class EmployeeRegistrationView(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = EmployeeSerializer(data=request.data)
        print("========================================================")
        print("ggggggggggggggggggggg", serializer)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        print(
            validated_data,
            "ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt",
        )

        email = validated_data.get("email")
        username = validated_data.get("username")
        # department = validated_data.get("department")
        print("============================0000000============================")
        designation = validated_data.get("designation")
        print(email, username, designation, "hhhhhhhhhhhhhhh")

        temporary_password = validated_data.get("temporaryPassword")

        # department = Department.objects.get(name=department)

        employee = Employee.objects.create(
            email=email,
            username=username,
            # department=department,
            designation=designation,
            password=make_password(temporary_password),
        )
        print("jjjjjjjjjjjjj")
        email_token = default_token_generator.make_token(employee)
        employee.email_token = email_token
        employee.save()

        tokens = generate_tokens(employee)

        accessToken = tokens["access"]

        send_email_to_employee(
            email, username, employee.id, temporary_password, accessToken
        )

        # print("successs", department)
        response_data = {
            "message": "Employee registered successfully.",
            "username": username,
            "email": email,
            "designation": designation,
            # "department": department.name,
            "temporaryPassword": temporary_password,
            "tokens": tokens,
        }

        return Response(response_data, status=status.HTTP_200_OK)


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def send_email_to_employee(email, username, user_id, temporary_password, email_token):
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


class ChangePass(APIView):
    def post(self, request, format=None):
        print(request.data, "hellooooo")
        oldpassword = request.data["oldpass"]
        password = request.data["password"]
        user_id = request.data["user_id"]
        print(oldpassword, password)
        user = Employee.objects.get(id=user_id)

        success = user.check_password(oldpassword)
        if success:
            user.set_password(password)
            user.save()
            print("updated")
            data = {"msg": 200}
            return Response(data)
        else:
            print("Not done")
            data = {"msg": 500}
            return Response(data)


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
            print(email, "emailllllllllll")
            # user =  Employee.objects.get(email=email)
            employee = Employee.objects.select_related("department").get(email=email)
            print(employee, "jjjjjjj")
            # department_name = employee.department.name
            print("here")
            print(employee, "im the bosssss")
            # print(department_name, "department is ourssssssss")
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
                # "department": department_name,
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


class EmployeeListView(APIView):
    def get(self, request):
        employees = Employee.objects.filter(is_superuser=False)
        serializer = EmployeeDisplaySerializer(employees, many=True)
        return Response(serializer.data)


class BlockEmployeeView(APIView):
    def put(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found")

        employee.is_active = False
        employee.is_blocked = True
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class UnblockEmployeeView(APIView):
    def put(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found")

        employee.is_active = True
        employee.is_blocked = False
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class EmployeeEditView(APIView):
    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)

            serializer = EmployeeDisplaySerializer(employee)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except employee.DoesNotExist:
            return Response(
                {"message": "employee not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)

            form_data = request.data.get("employee_name")
            # form_data = request.data.get('formDataToSend')

            serializer = EmployeeEditSerializer(
                employee, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except employee.DoesNotExist:
            return Response(
                {"message": "employee not found"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["PUT"])
def upload_profile_picture(request):
    user_id = request.data.get("user_id")
    try:
        employee = Employee.objects.get(id=user_id)
        image_file = request.FILES.get("profile_pic")
        if image_file:
            employee.profile_pic = image_file
            employee.save()
            serializer = EmployeePicSerializer(employee)
            return Response(serializer.data)
        else:
            return Response({"message": "No image file found"}, status=400)
    except Employee.DoesNotExist:
        return Response({"message": "User not found"}, status=404)


# class AdminSearchEmployee(ListCreateAPIView):
#     serializer_class = EmployeeSerializer
#     filter_backends = [SearchFilter]
#     queryset = Employee.objects.filter(is_superuser=False)
#     search_fields = ["username"]


class DepartmentListAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            department = self.get_object(pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)

        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = self.get_object(pk)
        employees = Employee.objects.filter(department=department)
        employees.update(department=None)
        department.delete()
        return Response(
            {"message": "Department deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(
                {"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["POST"])
def add_department(request):
    if request.method == "POST":
        serializer = DepartmentSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnouncementEditView(APIView):
    def get(self, request):
        announcements = Announcement.objects.all().values()
        return JsonResponse(list(announcements), safe=False)

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)

        if serializer.is_valid():
            print("success")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, announcement_id):
        try:
            announcement = Announcement.objects.get(id=announcement_id)
            announcement.delete()
            return JsonResponse(
                {"message": "Announcement deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Announcement.DoesNotExist:
            return JsonResponse(
                {"message": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND
            )
