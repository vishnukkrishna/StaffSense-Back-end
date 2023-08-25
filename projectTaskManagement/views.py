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

# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    print(queryset, "ggggggggggggggggggggggggggggggg")
    serializer_class = ProjectSerializer

    def create(self, request):
        name = request.data.get("name", None)

        if name:
            # name_lower = name.lower()

            if Project.objects.filter(
                name__iexact=name.lower().replace(" ", "")
            ).exists():
                return Response(
                    {"detail": "Project with this name already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "Project name is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["PUT"])
    def update_project(self, request, pk=None):
        print("i am hereeeeeeeeeeeeeeeeee")
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

        start_date_str = request_data.get("start_date")
        end_date_str = request_data.get("end_date")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if start_date < project.start_date or end_date > project.end_date:
            raise ValidationError(
                "Task's start date and end date must be within the project's start date and end date."
            )

        if project.task_set.filter(assignedTo=assigned_to).exists():
            raise ValidationError("Employee is already assigned to the project.")

        task = Task.objects.create(
            name=request_data.get("name"),
            description=request_data.get("description"),
            start_date=start_date,
            end_date=end_date,
            project=project,
        )
        task.assignedTo.set([assigned_to])

        return Response("successsss", status=status.HTTP_201_CREATED)

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
        print(task.state, "oooooooooooooooooooooooooooooooooo")
        task.save()
        print(task,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

        return Response(
            {"success": "Task status updated successfully."}, status=status.HTTP_200_OK
        )

    except Task.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
