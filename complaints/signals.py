from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Complaint
from .utils import send_complaint_email


@receiver(post_save, sender=Complaint)
def complaint_request_status_updated(sender, instance, created, **kwargs):
    if not created:
        if instance.status == "Resolved" or instance.status == "In Progress":
            send_complaint_email(
                instance.employee.email,
                instance.status,
            )
