from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from .utils import send_task_email

# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        name = request.data.get("name", None)
        assigned_to_id = request.data.get("assignedTo", None)

        if not name:
            return Response(
                {"detail": "Project name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            assigned_to = Employee.objects.get(id=assigned_to_id)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Assigned Employee not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for duplicate project names (case-insensitive, no spaces)
        if Project.objects.filter(name__iexact=name.lower().replace(" ", "")).exists():
            return Response(
                {"detail": "Project with this name already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project_data = {
            "name": name,
            "description": request.data.get("description", ""),
            "start_date": request.data.get("start_date", None),
            "end_date": request.data.get("end_date", None),
            "assignedTo": assigned_to,
        }

        project = Project(**project_data)
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def update_project(self, request, pk=None):
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["DELETE"])
    def delete_project(self, request, pk=None):
        project = self.get_object()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()

        # Convert 'assignedTo' value to an integer
        assigned_to_id = int(request_data.get("assignedTo", 0))
        assigned_to = get_object_or_404(Employee, pk=assigned_to_id)

        # Similarly, convert 'project' value to an integer
        project_id = int(request_data.get("project", 0))
        project = get_object_or_404(Project, pk=project_id)

        # Parse start_date and end_date
        start_date_str = request_data.get("start_date")
        end_date_str = request_data.get("end_date")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response("Invalid date format", status=status.HTTP_400_BAD_REQUEST)

        if start_date < project.start_date or end_date > project.end_date:
            return Response("Date Error", status=status.HTTP_400_BAD_REQUEST)

        # Create the task
        task = Task.objects.create(
            name=request_data.get("name"),
            description=request_data.get("description"),
            start_date=start_date,
            end_date=end_date,
            project=project,
        )
        task.assignedTo.set([assigned_to])

        # After creating the task, send the email notification
        send_task_email(
            user_email=assigned_to.email,
            name=task.name,
            assignedTo=assigned_to.first_name,  # Assuming you want to use the first name
            start_date=start_date,
            end_date=end_date,
        )

        return Response("success", status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def individual_task(request, pk):
    try:
        user = Employee.objects.get(id=pk)
        tasks = Task.objects.filter(assignedTo=user)
        serializer = TaskSerializer(
            tasks, many=True
        )  # Pass many=True for multiple tasks
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except Task.DoesNotExist:
        return Response(
            {"error": "No tasks found for the employee."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
def update_task_status(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        new_status = request.data.get("status")
        task.state = new_status
        task.save()
        return Response(
            {"success": "Task status updated successfully."}, status=status.HTTP_200_OK
        )
    except Task.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
