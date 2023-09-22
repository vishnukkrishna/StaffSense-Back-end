from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from .utils import send_block_email


@receiver(post_save, sender=Employee)
def employee_blocked(sender, instance, created, **kwargs):
    if not created:
        send_block_email(
            instance.employee.email,
            instance.is_blocked,
        )
