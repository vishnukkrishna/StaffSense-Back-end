from django.db import models
from django.utils import timezone
from authentication.models import Employee
import uuid
from django.core.validators import EmailValidator

# Create your models here.


class Visitor(models.Model):
    name = models.CharField(max_length=255)
    reason = models.TextField()
    email = models.EmailField(validators=[EmailValidator()])
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    checked_in = models.BooleanField(default=False)
    organizer = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visitors",
    )

    def __str__(self):
        return f"{self.name} -Reason- {self.reason} -Date {self.date} {self.start_time} to {self.end_time}"
