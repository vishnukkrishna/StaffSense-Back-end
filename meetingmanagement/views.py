from django.shortcuts import render
from .models import *
from authentication.models import Employee
from .serializers import MeetingSerializer, MeetingOrganizerSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Q

# Create your views here.


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.select_related("organizer")
    serializer_class = MeetingOrganizerSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return MeetingSerializer
        return MeetingOrganizerSerializer

    def list(self, request, *args, **kwargs):
        meetings = self.get_queryset()
        serializer = self.get_serializer(meetings, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        start_time = request.data.get("start_time")

        end_time = request.data.get("end_time")
        date = request.data.get("date")

        conflicting_bookings = Meeting.objects.filter(
            Q(date=date) & Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
        )

        if conflicting_bookings.exists():
            return Response(
                {"error": "Booking conflicts with existing meetings"},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)

        except Exception as e:
            print("here", e)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")
        conflicting_bookings = Meeting.objects.filter(
            start_time__lt=end_time, end_time__gt=start_time
        ).exclude(id=instance.id)
        if conflicting_bookings.exists():
            return Response(
                {"error": "Booking conflicts with existing meetings"},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
