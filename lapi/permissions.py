from rest_framework.permissions import BasePermission

from authentication.utils import get_my_object
from users.models import Teacher


class MediaOwnerTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.course.teacher == get_my_object(request, Teacher):
            return True
        elif obj.seminar.teacher == get_my_object(request, Teacher):
            return True
        elif obj.post.author == get_my_object(request, Teacher):
            return True
        return False
