from rest_framework import serializers
from .models import Project, Task
from projectTaskManagement.models import Employee


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    assignedTo = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Project
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    assignedTo = EmployeeSerializers(many=True)
    project = ProjectSerializer()

    class Meta:
        model = Task
        fields = "__all__"
