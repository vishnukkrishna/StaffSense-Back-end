from .models import *
from rest_framework import serializers
from authentication.serializers import *
from rest_framework.serializers import SerializerMethodField


class ChatSerializer(serializers.ModelSerializer):
    sender_username = SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["message", "sender_username"]

    def get_sender_username(self, obj):
        return obj.sender.username


class ChatListSerializer(serializers.ModelSerializer):
    user_profile = SerializerMethodField
    username = SerializerMethodField

    class Meta:
        model = Chat
        fields = ["user_profile", "username"]

    def get_username(self, obj):
        return obj

    def get_user_profile(self, obj):
        return EmployeeDisplaySerializer(
            Employee.objects.filter(user__username=obj).first()
        ).data.get("profile_pic")
