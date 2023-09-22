from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import send_complaint_emal
from rest_framework import viewsets
from .models import Complaint
from authentication.models import Employee
from complaints.serializer import ComplaintSerializer, ComplaintsSerializer

# Create your views here.


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().order_by("id")
    serializer_class = ComplaintSerializer

    def create(self, request, *args, **kwargs):
        employee_id = request.data.get("employee")
        description = request.data.get("description")
        is_present = request.data.get("is_present")

        complaint_data = {
            "employee": employee_id,
            "description": description,
            "is_present": is_present,
        }

        serializer = self.get_serializer(data=complaint_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        original_status = instance.status
        self.perform_update(serializer)
        if original_status != instance.status and instance.status in [
            "Resolved",
            "In Progress",
        ]:
            send_complaint_emal(instance.employee.email, instance.status)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().select_related("employee"))
        serializer = ComplaintsSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def user_complaint_list(request, employee_id):
    complaints = Complaint.objects.filter(employee_id=employee_id)
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)
