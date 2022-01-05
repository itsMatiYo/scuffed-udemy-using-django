from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from authentication.utils import (get_token, get_wallet_and_verify_token,
                                  verify_token, verify_token_for_admin)
from users import models


class StudentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            wallet = get_wallet_and_verify_token(request=request)
        except:
            return False
        return models.Student.objects.filter(wallet=wallet).exists()


class TeacherPermissionUnApproved(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            wallet = get_wallet_and_verify_token(request=request)
        except:
            return False
        return models.Teacher.objects.filter(wallet=wallet).exists()


class TeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            wallet = get_wallet_and_verify_token(request=request)
        except:
            return False
        try:
            teacher = models.Teacher.objects.get(wallet=wallet)
            return teacher.approved
        except:
            return False


class AdviserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            wallet = get_wallet_and_verify_token(request=request)
        except:
            return False
        try:
            adviser = models.Adviser.get(wallet=wallet)
            return adviser.approved
        except:
            return False


class AdviserPermissionUnApproved(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            wallet = get_wallet_and_verify_token(request=request)
        except:
            return False
        return models.Adviser.objects.filter(wallet=wallet).exists()


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        return verify_token_for_admin(token)


class AdminOrUserReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if request.method in SAFE_METHODS:
            return True
        else:
            return verify_token_for_admin(token)


class Admin_And_User(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if verify_token_for_admin(token) or verify_token(token):
            return True
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
