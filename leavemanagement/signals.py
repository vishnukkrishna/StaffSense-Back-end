from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest
from .utils import send_leave_email


@receiver(post_save, sender=LeaveRequest)
def leave_request_status_updated(sender, instance, created, **kwargs):
    if not created:
        send_leave_email(
            instance.employee.email,
            instance.is_approved,
            instance.start_date,
            instance.end_date,
        )
