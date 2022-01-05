from rest_framework import serializers


class ChatCreateSrializer(serializers.Serializer):

    type = serializers.CharField()
    admin_usernames = serializers.ListSerializer(
        child=serializers.CharField())
    usernames = serializers.ListSerializer(
        child=serializers.CharField())


class ChatAddUserSrializer(serializers.Serializer):

    chat = serializers.CharField()
    username = serializers.CharField()


class UploadeFileSerializer(serializers.Serializer):

    file = serializers.FileField()
