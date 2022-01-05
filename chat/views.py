from decouple import config
from rest_framework import exceptions
from rest_framework.views import APIView

from authentication.permission import Admin_And_User, AdminPermission
from authentication.utils import send_request_to_server
from chat.serializer import (ChatAddUserSrializer, ChatCreateSrializer,
                             UploadeFileSerializer)

# * Server Information :
HOST_CHAT = config('HOST_CHAT')
TOKEN = config('TOKEN')


# * Chat : Create Chat
class ChatCreate(APIView):
    permission_classes = [AdminPermission]
    serializer_class = ChatCreateSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = HOST_CHAT + "/chat/create"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Chat : Add User to Chat
class UserAdd(APIView):
    permission_classes = [AdminPermission]
    serializer_class = ChatAddUserSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = HOST_CHAT + "/chat/add-user"
            return send_request_to_server(url=url, serializer=serializer, request_type="post")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Chat : Uploade File
class FileUploade(APIView):
    permission_classes = [Admin_And_User]
    serializer_class = UploadeFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = HOST_CHAT + "/upload/file"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", data_type="files")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)
