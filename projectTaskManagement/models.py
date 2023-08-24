from django.db import models
from authentication.models import *

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    STATUS = (
        ("NEW", "NEW"),
        ("PENDING", "PENDING"),
        ("IN PROGRESS", "IN PROGRESS"),
        ("COMPLETED", "COMPLETED"),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    assignedTo = models.ManyToManyField(Employee)

    state = models.CharField(max_length=11, choices=STATUS, default="NEW")

    def __str__(self):
        return str(self.name)
