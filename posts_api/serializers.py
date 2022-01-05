from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.serializers import StudentSerializer, TeacherCategoryPatch

from .models import *


class CommentSerializer(ModelSerializer):
    author = StudentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['approved', ]


class PostSerializer(ModelSerializer):
    author = TeacherCategoryPatch(read_only=True)
    likes = StudentSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('likes', 'approved',)


class PostCopySerializer4Teacher(ModelSerializer):
    class Meta:
        model = PostCopy
        fields = '__all__'


# ! Admin Serializers
class CommentSerializer4Admin(ModelSerializer):
    author = StudentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer4Admin(ModelSerializer):
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    author = TeacherCategoryPatch(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCopySerializer4Admin(ModelSerializer):
    class Meta:
        model = PostCopy
        fields = '__all__'
