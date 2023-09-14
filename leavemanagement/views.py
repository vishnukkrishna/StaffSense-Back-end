from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeaveRequest
from .serializers import *
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from authentication.models import *
from .utils import send_leave_email
from rest_framework.decorators import api_view

# Create your views here.


class LeaveApplicationView(APIView):
    def post(self, request, format=None):
        employee = request.data.get("employee")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        employee_id = Employee.objects.get(pk=employee)

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date and start_date < date.today():
            return Response(
                {"error": "You cannot apply for leave in the past."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if employee_id and start_date and end_date:
            existing_leave = LeaveRequest.objects.filter(
                employee=employee_id, start_date__lte=end_date, end_date__gte=start_date
            ).exists()

            if existing_leave:
                return Response(
                    {"error": "You have already applied for leave during this period."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = LeaveSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        leaves = LeaveRequest.objects.all()
        serializer = LeaveWithEmployeeSerializer(leaves, many=True)

        data = serializer.data
        return Response(data)

    def put(self, request, format=None):
        leave_id = request.data.get("leave_id")
        leave = LeaveRequest.objects.get(id=leave_id)
        is_approved = request.data.get("is_approved")
        start_date = leave.start_date
        end_date = leave.end_date
        user_email = request.data.get("email")

        leave_request = get_object_or_404(LeaveRequest, pk=leave_id)
        leave_request.is_approved = is_approved
        leave_request.save()
        send_leave_email(user_email, is_approved, start_date, end_date)

        return Response(
            {"message": "Leave request status updated successfully."},
            status=status.HTTP_200_OK,
        )


class UserLeaveDataView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get("employee")
        if not user_id:
            return Response({"error": "Please provide the employee ID."}, status=400)

        leave_data = LeaveRequest.objects.filter(employee_id=user_id)
        serializer = LeaveSerializer(leave_data, many=True)

        return Response(serializer.data)


class UserLeaveDataView(APIView):
    def get(self, request, employee_id):
        leave_data = LeaveRequest.objects.filter(
            employee_id=employee_id, is_approved=True
        )

        serializer = LeaveSerializer(leave_data, many=True)

        return Response(serializer.data)


@api_view(["GET"])
def get_employee_leave_requests(request, employee_id):
    try:
        leave_requests = LeaveRequest.objects.filter(employee_id=employee_id).order_by(
            "-start_date"
        )

        serializer = LeaveSerializer(leave_requests, many=True)

        return Response(serializer.data, status=200)
    except LeaveRequest.DoesNotExist:
        return Response({"error": "Leave requests not found."}, status=404)


class DashboardDataAPIView(APIView):
    def get(self, request, format=None):
        employee_count = Employee.objects.all().count()
        department_count = Department.objects.all().count()
        # visitors_count = Visitor.objects.all().count()

        data = {
            "employeeCount": employee_count,
            "departmentCount": department_count,
            # "visitorsCount": visitors_count,
        }

        return Response(data)
