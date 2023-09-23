from django.db import models
from authentication.models import Employee

# Create your models here.


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    organizer = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
