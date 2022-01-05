from rest_framework.permissions import BasePermission

from authentication.utils import get_my_object, get_token, get_wallet
from users import models


class TeacherIsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            wallet = models.Wallet.objects.get(id=str(wallet.id))
            owner = models.Teacher.objects.get(wallet=wallet)
            if obj.teacher == owner:
                return True
        except:
            return False


class StudentIsInClassFile(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            wallet = models.Wallet.objects.get(id=str(wallet.id))
            student = models.Student.objects.get(wallet=wallet)
            if student in obj.course.students.all():
                return True
        except:
            return False


class TeacherDotCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            wallet = models.Wallet.objects.get(id=str(wallet.id))
            teacher = models.Teacher.objects.get(wallet=wallet)
            if obj.course.teacher == teacher:
                return True
        except:
            return False


class TeacherIsExamOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            wallet = models.Wallet.objects.get(id=str(wallet.id))
            teacher = models.Teacher.objects.get(wallet=wallet)
            if obj.course.teacher == teacher:
                return True
        except:
            return False


class TeacherIsAnswerFileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            wallet = models.Wallet.objects.get(id=str(wallet.id))
            teacher = models.Teacher.objects.get(wallet=wallet)
            if obj.exam.course.teacher == teacher:
                return True
            else:
                return False
        except:
            return False


class StudentIsAnswerFileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            wallet = models.Wallet.objects.get(id=str(wallet.id))
            student = models.Student.objects.get(wallet=wallet)
            return student == obj.student
        except:
            return False


class StudentInCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token = get_token(request)
            wallet = get_wallet(token)
            wallet = models.Wallet.objects.get(id=str(wallet.id))
            student = models.Student.objects.get(wallet=wallet)
            return student in obj.students.all()
        except:
            return False


class TeacherIsTimesOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        tea = get_my_object(request, models.Teacher)
        return obj.seminar.teacher == tea
