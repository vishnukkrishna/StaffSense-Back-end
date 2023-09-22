from django.db import models
from authentication.models import Employee

# Create your models here.


class Complaint(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        # Add more complaint reasons types as needed
    ]
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.employee} - {self.description} - {self.status}"
