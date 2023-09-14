from django.db import models
from authentication.models import Employee


# Create your models here.
class LeaveRequest(models.Model):
    LEAVE_TYPES = (
        ("Sick Leave", "Sick Leave"),
        ("Vacation Leave", "Vacation Leave"),
        ("Personal Leave", "Personal Leave"),
        # Add more leave types as needed
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(choices=LEAVE_TYPES, max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} - {self.start_date} to {self.end_date}"
