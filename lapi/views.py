from django.http import request
from rest_framework import exceptions, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework import status

from authentication.permission import (
    AdminPermission,
    ReadOnly,
    StudentPermission,
    TeacherPermission,
)
from authentication.utils import (
    get_my_object,
    is_it_admin,
    is_it_adviser,
    is_it_student,
    is_it_teacher,
)
from course.models import Ticket4Seminar
from lapi import models, serializers
from lapi.models import Attrib, Category, Media
from lapi.permissions import MediaOwnerTeacher
from users.models import Adviser, Student, Teacher


class CategoryList(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    filterset_fields = (
        "name",
        "level",
        "parent",
    )

    serializer_class = serializers.CategorySerializer
    # is admin or read only
    permission_classes = [AdminPermission | ReadOnly]

    def get(self, request, *args, **kwargs):
        self.serializer_class = serializers.CategoryListSerializer
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            parent_level = models.Category.objects.get(
                pk=self.request.data.get("parent")
            ).level
            return serializer.save(level=int(parent_level) + 1)
        except:
            return serializer.save(level=0)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    # is admin or read only
    permission_classes = [AdminPermission | ReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            req = self.request
            pk = self.kwargs.get("pk")
            category = models.Category.objects.get(pk=self.kwargs.get("pk"))
            if is_it_admin(req):
                return serializers.CategorySerializer
            elif is_it_teacher(req):
                teacher = get_my_object(req, Teacher)
                if category in teacher.attribs.category.all():
                    return serializers.CategoryTeacherSerializer
            elif is_it_adviser(req):
                adviser = get_my_object(req, Adviser)
                if adviser.category == category:
                    return serializers.CategoryAdviserSerializer
            else:
                return serializers.CategoryListSerializer
        else:
            return serializers.CategorySerializer

    def patch(self, request, *args, **kwargs):
        self.serializer_class = serializers.CategorySerializerPatch
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        raise exceptions.ValidationError("You can't use put request on this object.")

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if Attrib.objects.filter(category=obj).exists():
            return Response(
                {"Attrib": "You cannot delete this category because it has attribs"},
                status=status.HTTP_226_IM_USED,
            )
        elif Category.objects.filter(parent=obj).exists():
            return Response(
                {
                    "Parent": "You cannot delete this category because it has children(subcategories)"
                },
                status=status.HTTP_226_IM_USED,
            )
        else:
            return super().destroy(request, *args, **kwargs)


class AttribDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Attrib.objects.all()
    serializer_class = serializers.AttribSerializer
    # is admin or read only
    permission_classes = [AdminPermission | ReadOnly]

    def patch(self, request, *args, **kwargs):
        self.serializer_class = serializers.AttribSerializerPatch
        return self.partial_update(request, *args, **kwargs)


class AttribList(generics.ListCreateAPIView):
    queryset = models.Attrib.objects.all()
    serializer_class = serializers.AttribSerializer
    # is admin or read only
    permission_classes = [AdminPermission | ReadOnly]
    filterset_fields = ["category"]


class UserTicket(generics.ListAPIView):
    queryset = Ticket4Seminar.objects.all()
    serializer_class = serializers.Ticket4SeminarSerializer
    permission_classes = [StudentPermission | AdminPermission]

    def get_queryset(self):
        if is_it_student(self.request):
            student = get_my_object(self.request, Student)
            return Ticket4Seminar.objects.filter(student=student)
        else:
            return Ticket4Seminar.objects.all()


class MediaList(generics.ListCreateAPIView):
    permission_classes = [AdminPermission | TeacherPermission | ReadOnly]
    queryset = models.Media.objects.all()
    serializer_class = serializers.MediaSerializer

    def perform_create(self, serializer):
        if is_it_teacher(request):
            course = serializer.validated_data.get("course")
            seminar = serializer.validated_data.get("seminar")
            teacher = get_my_object(request, Teacher)
            post = serializer.validated_data.get("post")
            if seminar:
                if teacher == seminar.teacher:
                    return serializer.save()
            elif course:
                if teacher == course.teacher:
                    return serializer.save()
            elif post:
                if teacher == post.author:
                    return serializer.save()
            else:
                raise serializers.ValidationError(
                    "You do not own this seminar or course"
                )
        else:
            return serializer.save()


class MediaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        AdminPermission | (TeacherPermission & MediaOwnerTeacher) | ReadOnly
    ]
    queryset = models.Media.objects.all()
    serializer_class = serializers.MediaSerializer

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [AdminPermission]
        return super().delete(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            if is_it_teacher(self.request):
                return serializers.MediaSerializerUpdate
            else:
                return serializers.MediaSerializerUpdate4Admin
        else:
            return super().get_serializer_class()

    def perform_update(self, serializer):
        if is_it_teacher(self.request):
            return serializer.save(approved=False)
        else:
            return serializer.save()


class CompanyInfoViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = models.CompanyInfo.objects.all()
    serializer_class = serializers.CompanyInfoSerializer
    permission_classes = [AdminPermission | ReadOnly]

    def perform_create(self, serializer):
        try:
            models.CompanyInfo.objects.get(id=1)
        except:
            return super().perform_create(serializer)
        raise exceptions.ValidationError({"Unique": "This object is already available"})
