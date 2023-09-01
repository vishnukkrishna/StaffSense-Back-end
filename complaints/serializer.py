from rest_framework import serializers
from complaints.models import Complaint
from authentication.models import Employee


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"


class EmployeeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "username", "email"]


class ComplaintsSerializer(serializers.ModelSerializer):
    employee = EmployeeFieldSerializer()

    class Meta:
        model = Complaint
        fields = ["id", "description", "is_present", "status", "employee"]
