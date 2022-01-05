from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission import (
    AdminPermission,
    ReadOnly,
    StudentPermission,
    TeacherPermission,
)
from authentication.utils import get_my_object, is_it_student, is_it_teacher
from posts_api.permissions import (
    StudentIsAuthorComment,
    TeacherIsAuthor,
    TeacherIsAuthorCopy,
)
from users.models import Student, Teacher

from .models import *
from .serializers import *


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [TeacherPermission | ReadOnly]
    filterset_fields = [
        "author",
        "created_at",
    ]

    def get_queryset(self):
        if is_it_teacher(self.request):
            return Post.objects.filter(
                Q(approved=True) | Q(author=get_my_object(self.request, Teacher))
            )
        return Post.objects.filter(approved=True)

    def perform_create(self, serializer):
        teacher = get_my_object(self.request, Teacher)
        return serializer.save(author=teacher)


class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [(TeacherPermission & TeacherIsAuthor) | ReadOnly]

    def get_queryset(self):
        if is_it_teacher(self.request):
            return Post.objects.filter(
                Q(approved=True) | Q(author=get_my_object(self.request, Teacher))
            )
        return Post.objects.filter(approved=True)


class PostCopyList(generics.ListCreateAPIView):
    serializer_class = PostCopySerializer4Teacher
    permission_classes = [TeacherPermission]
    queryset = PostCopy.objects.all()
    filterset_fields = [
        "delete_request",
    ]

    def get_queryset(self):
        req = self.request
        if req.method == "GET":
            return PostCopy.objects.filter(
                post__author=get_my_object(self.request, Teacher)
            )
        else:
            return self.queryset

    def perform_create(self, serializer):
        post = serializer.validated_data.get("post")
        if post.author == get_my_object(self.request, Teacher):
            return serializer.save()
        else:
            raise PermissionDenied("You don't own this post")


class PostCopyDetail(generics.RetrieveDestroyAPIView):
    queryset = PostCopy.objects.all()
    serializer_class = PostCopySerializer4Teacher
    permission_classes = [TeacherPermission & TeacherIsAuthorCopy]

    def get_queryset(self):
        req = self.request
        if req.method == "GET":
            return PostCopy.objects.filter(
                post__author=get_my_object(self.request, Teacher)
            )
        return self.queryset


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(approved=True)
    serializer_class = CommentSerializer
    filterset_fields = (
        "post",
        "reply_to",
    )
    permission_classes = [StudentPermission | ReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=get_my_object(self.request, Student))

    def get_queryset(self):
        req = self.request
        if is_it_student(req):
            return Comment.objects.filter(
                Q(approved=True) | Q(author=get_my_object(req, Student))
            )
        return super().get_queryset()


class CommentDetail(generics.RetrieveDestroyAPIView):

    queryset = Comment.objects.filter(approved=True)
    serializer_class = CommentSerializer
    permission_classes = [(StudentPermission & StudentIsAuthorComment) | ReadOnly]


class PostLike(APIView):
    permission_classes = [StudentPermission]

    def get(self, request, *args, **kwargs):
        post_id = kwargs["id"]
        student_obj = get_my_object(request, Student)
        post_obj = get_object_or_404(Post, id=post_id, approved=True)
        try:
            post_obj.likes.add(student_obj)
        except:
            raise exceptions.ValidationError(detail="can't do this", code=400)
        return Response(status=200)


class PostDisLike(APIView):
    permission_classes = [StudentPermission]

    def get(self, request, *args, **kwargs):
        post_id = kwargs["id"]
        student_obj = get_my_object(request, Student)
        post_obj = get_object_or_404(Post, id=post_id, approved=True)
        try:
            post_obj.likes.remove(student_obj)
        except:
            raise exceptions.ValidationError(detail="can't do this", code=400)
        return Response(status=200)


# ! admin viewsets
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer4Admin
    permission_classes = [AdminPermission]
    filterset_fields = (
        "post",
        "reply_to",
        "approved",
    )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer4Admin
    permission_classes = [AdminPermission]
    filterset_fields = ("author",)


class PostCopyViewSet(viewsets.ModelViewSet):
    queryset = PostCopy.objects.all()
    serializer_class = PostCopySerializer4Admin
    permission_classes = [AdminPermission]
