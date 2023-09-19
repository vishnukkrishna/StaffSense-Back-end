from rest_framework import serializers
from authentication.models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class EmployeeSerializer(serializers.ModelSerializer):
    temporaryPassword = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["username", "email", "temporaryPassword", "department", "designation"]


class EmployeeDisplaySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Employee

        fields = [
            "id",
            "department_id",
            "department_name",
            "first_name",
            "last_name",
            "username",
            "phone",
            "email",
            "profile_pic",
            "designation",
            "is_blocked",
        ]


class EmployeeEditSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source="department", write_only=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "department_id",
            "department_name",
            "first_name",
            "last_name",
            "username",
            "phone",
            "email",
            "designation",
            "is_blocked",
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user or not user.is_superuser:
            raise serializers.ValidationError("Invalid credentials.")

        refresh = RefreshToken.for_user(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserDataSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "email",
            "department",
            "designation",
            "first_name",
            "last_name",
            "phone",
            "profile_pic",
        ]


class EmployeePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "profile_pic"]


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["event", "note"]
