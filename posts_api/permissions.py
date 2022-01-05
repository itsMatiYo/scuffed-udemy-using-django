from rest_framework.permissions import BasePermission

from authentication.utils import get_token, get_wallet
from users import models


class TeacherIsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            owner = models.Teacher.objects.get(wallet=wallet)
            if obj.author == owner:
                return True
        except:
            return False


class TeacherIsAuthorCopy(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            owner = models.Teacher.objects.get(wallet=wallet)
            if obj.post.author == owner:
                return True
        except:
            return False


class StudentIsAuthorComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            stu = models.Student.objects.get(wallet=wallet)
            if obj.author == stu:
                return True
        except:
            return False
