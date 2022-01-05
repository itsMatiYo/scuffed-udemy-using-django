from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lapi.models import Ticket4Adviser
from users.models import Adviser, Document, Student, Teacher, Wallet


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class Document_Serializer(ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = (
            "status",
            "reason",
        )


class Admin_Document_Serializer(ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class TicketSerializer(ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Ticket4Adviser
        fields = "__all__"


class AdviserCategoryPatch(ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Adviser
        fields = "__all__"
        read_only_fields = (
            "wallet",
            "document",
        )


class TeacherCategoryPatch(ModelSerializer):
    wallet = WalletSerializer(read_only=True)
    courses = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    seminars = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = (
            "wallet",
            "document",
        )


class StudentSerializer(ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"


class StudentSerializerAdmin(ModelSerializer):
    wallet = WalletSerializer(read_only=True)
    courses = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    seminars = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    ticket4seminar_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Student
        fields = "__all__"
