from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from authentication.models import *
from authentication.serializers import *
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.generics import *


@api_view(["GET"])
def Adminfetch(request):
    try:
        admin = Employee.objects.get(is_superuser=True)
        adminId = admin.id
        return Response({"admin_id": adminId}, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"message": "Admin not found"}, status=status.HTTP_404_NOT_FOUND
        )


class PreviousMessagesView(ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user1 = int(self.kwargs["user1"])
        user2 = int(self.kwargs["user2"])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = "chat_" + thread_suffix
        queryset = Chat.objects.filter(thread_name=thread_name)
        return queryset


