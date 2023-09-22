import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from .serializers import ChatSerializer
from .models import Chat
from authentication.models import *


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        current_user_id = int(self.scope["query_string"])
        other_user_id = self.scope["url_route"]["kwargs"]["id"]
        self.room_name = (
            f"{current_user_id}_{other_user_id}"
            if current_user_id > other_user_id
            else f"{other_user_id}_{current_user_id}"
        )

        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        sender_username = data["senderUsername"]
        receiver_username = data["receiverUsername"]

        await self.save_message(
            sender_username, receiver_username, message, self.room_group_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "senderUsername": sender_username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["senderUsername"]

        await self.send_json(
            {
                "message": message,
                "senderUsername": username,
                "messages": message,
            }
        )

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message, thread_name):
        try:
            sender_instance = Employee.objects.get(username=sender_username)
            receiver_instance = Employee.objects.get(username=receiver_username)

            Chat.objects.create(
                sender=sender_instance,
                receiver=receiver_instance,
                message=message,
                thread_name=thread_name,
            )
        except Employee.DoesNotExist:
            pass  # Handle the case when sender or receiver does not exist

    @database_sync_to_async
    def get_messages(self):
        messages = []

        for instance in Chat.objects.filter(thread_name=self.room_group_name):
            messages.append(ChatSerializer(instance).data)

        return messages
