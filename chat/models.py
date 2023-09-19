from django.db import models
from authentication.models import *

# Create your models here.


class Chat(models.Model):
    sender = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sender_message",
    )
    receiver = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reciever_message",
    )
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"{self.sender.username}-{self.thread_name}"
            if self.sender
            else f"{self.message}-{self.thread_name}"
        )
