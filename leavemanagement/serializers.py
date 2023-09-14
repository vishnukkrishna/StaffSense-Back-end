from rest_framework import serializers
from .models import LeaveRequest
from authentication.serializers import UserDataSerializer, DepartmentSerializer


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = "__all__"


class LeaveWithEmployeeSerializer(serializers.ModelSerializer):
    employee = UserDataSerializer()
    department = DepartmentSerializer(source="employee.department")

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",
            "department",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "is_approved",
        ]
