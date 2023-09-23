from .models import *
from rest_framework import serializers
from authentication.models import Employee


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["username", "department"]


class MeetingOrganizerSerializer(serializers.ModelSerializer):
    organizer_details = EmployeeDetailSerializer(source="organizer")

    class Meta:
        model = Meeting
        fields = [
            "id",
            "title",
            "description",
            "date",
            "start_time",
            "end_time",
            "organizer_details",
        ]
