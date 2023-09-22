from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from .utils import send_task_email


@receiver(post_save, sender=Task)
def task_created(sender, instance, created, **kwargs):
    if not created:
        send_task_email(
            instance.employee.email,
            instance.assignedTo,
            instance.start_date,
            instance.end_date,
        )
