import json
import datetime
from django.db.models.query_utils import Q

import jwt
from decouple import config
from rest_framework.test import APITestCase
from rest_framework import status

from posts_api import models as md
from posts_api.serializers import (
    CommentSerializer,
    CommentSerializer4Admin,
    PostCopySerializer4Admin,
    PostCopySerializer4Teacher,
    PostSerializer,
    PostSerializer4Admin,
)
from users.models import Student, Wallet, Teacher
from .utils import make_admin_token, make_token


class AdminViewTest(APITestCase):
    def setUp(self) -> None:

        wallet1 = Wallet.objects.create(id="test wallet id")
        teacher1 = Teacher.objects.create(wallet=wallet1, approved=True)
        student1 = Student.objects.create(wallet=wallet1)

        self.post1 = md.Post.objects.create(
            title="Post 2 Title",
            content="post 3 content",
            seo={},
            author=teacher1,
            approved=True,
        )
        self.post2 = md.Post.objects.create(
            title="Post 3 Title",
            content="post 2 content",
            seo={},
            approved=True,
        )
        self.post3 = md.Post.objects.create(
            title="Post 3 Title",
            content="post 3 content",
            seo={},
            approved=False,
        )

        self.postcopy1 = md.PostCopy.objects.create(
            title="Test post copy",
            content="Content of post copy1 ",
            post=self.post1,
            delete_request=True,
        )

        self.comment1 = md.Comment.objects.create(
            content="comment 1 content", author=student1, post=self.post2, approved=True
        )
        self.comment2 = md.Comment.objects.create(
            content="comment 2 content", author=student1, post=self.post2, approved=True
        )

        self.tokenAdmin = make_admin_token()

    def test_admin_post_get_all(self):
        response = self.client.get(
            "/posts/admin/post/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        posts = md.Post.objects.all()
        serializer = PostSerializer4Admin(posts, many=True)
        self.assertEqual(serializer.data, json.loads(response.content)["results"])

    def test_admin_post_get(self):
        res = self.client.get(
            f"/posts/admin/post/{self.post1.pk}/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        self.assertEqual(PostSerializer4Admin(self.post1).data, json.loads(res.content))

    def test_admin_post_update(self):
        res = self.client.patch(
            f"/posts/admin/post/{self.post1.pk}/",
            data={"approved": "False"},
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        self.assertEqual(self.post1.approved, True)

    def test_admin_post_delete(self):
        res = self.client.delete(
            f"/posts/admin/post/{self.post1.pk}/",
            data={"approved": "False"},
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_postcopy_get_all(self):
        res = self.client.get(
            "/posts/admin/postcopy/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        postcopies = md.PostCopy.objects.all()
        serializer = PostCopySerializer4Admin(postcopies, many=True)
        self.assertEqual(serializer.data, json.loads(res.content)["results"])

    def test_admin_postcopy_get(self):
        res = self.client.get(
            f"/posts/admin/postcopy/{self.postcopy1.pk}/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        serializer = PostCopySerializer4Admin(self.postcopy1)
        self.assertEqual(serializer.data, json.loads(res.content))

    def test_admin_postcopy_delete(self):
        res = self.client.delete(
            f"/posts/admin/postcopy/{self.postcopy1.pk}/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_comment_get_all(self):
        res = self.client.get(
            "/posts/admin/comment/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )

        comments = md.Comment.objects.all()
        serializer = CommentSerializer4Admin(comments, many=True)
        self.assertEqual(serializer.data, json.loads(res.content)["results"])

    def test_admin_comment_get(self):
        res = self.client.get(
            f"/posts/admin/comment/{self.comment1.pk}/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )
        serializer = CommentSerializer4Admin(self.comment1)
        self.assertEqual(serializer.data, json.loads(res.content))

    def test_admin_comment_delete(self):
        res = self.client.delete(
            f"/posts/admin/comment/{self.comment1.pk}/",
            HTTP_AUTHORIZATION=self.tokenAdmin,
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)


class TeacherViewTest(APITestCase):
    def setUp(self) -> None:
        wallet1 = Wallet.objects.create(id="test wallet id")
        wallet2 = Wallet.objects.create(id="test wallet id 2")
        self.teacher1 = Teacher.objects.create(wallet=wallet1, approved=True)
        self.teacher2 = Teacher.objects.create(wallet=wallet2, approved=False)

        self.post1 = md.Post.objects.create(
            title="sdsd", content="content", approved=True, author=self.teacher1
        )
        self.post2 = md.Post.objects.create(
            title="sdsd",
            content="content",
        )
        self.post3 = md.Post.objects.create(
            title="sdsd", content="content", approved=True, author=self.teacher1
        )
        self.copypost1 = md.PostCopy.objects.create(
            title="sdsd",
            content="test",
            post=self.post1,
        )
        self.copypost2 = md.PostCopy.objects.create(
            title="sdsd",
            content="test",
            post=self.post2,
        )

    def test_teacher_post_create(self):
        res = self.client.post(
            "/posts/",
            data={"title": "Test Teacher", "content": "Content 1 Teacher 1"},
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_unapproved_teacher_post_create(self):
        res = self.client.post(
            "/posts/",
            data={"title": "Test Teacher", "content": "Content 1 Teacher 1"},
            HTTP_AUTHORIZATION=make_token(self.teacher2),
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_post_get_all(self):
        res = self.client.get(
            "/posts/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        posts = md.Post.objects.filter(Q(author=self.teacher1) | Q(approved=True))
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(serializer.data, json.loads(res.content)["results"])

    def test_teacher_post_get(self):
        res = self.client.get(
            f"/posts/{self.post1.pk}/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )

        serializer = PostSerializer(self.post1)
        self.assertEqual(serializer.data, json.loads(res.content))

    def test_teacher_postcopy_create(self):
        res = self.client.post(
            "/posts/copy/",
            data={"title": "11s", "content": "sdsd", "post": f"{self.post3.pk}"},
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_teacher_postcopy_not_owner_create(self):
        res = self.client.post(
            "/posts/copy/",
            data={"title": "11s", "content": "sdsd", "post": f"{self.post2.pk}"},
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_teacher_postcopy_get_all(self):
        res = self.client.get(
            "/posts/copy/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        postcopies = md.PostCopy.objects.filter(post__author=self.teacher1)
        serializer = PostCopySerializer4Teacher(postcopies, many=True)
        self.assertEqual(serializer.data, json.loads(res.content)["results"])

    def test_teacher_postcopy_get(self):
        res = self.client.get(
            f"/posts/copy/{self.copypost1.pk}/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        serializer = PostCopySerializer4Teacher(self.copypost1)
        self.assertEqual(serializer.data, json.loads(res.content))

    def test_teacher_postcopy_now_owner_get(self):
        res = self.client.get(
            f"/posts/copy/{self.copypost2.pk}/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_teacher_postcopy_delete(self):
        res = self.client.delete(
            f"/posts/copy/{self.copypost1.pk}/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_postcopy_not_owner_delete(self):
        res = self.client.delete(
            f"/posts/copy/{self.copypost2.pk}/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_comment_create(self):
        wallet = Wallet.objects.create(id="sddsd1123")
        st1 = Student.objects.create(wallet=wallet)
        res = self.client.post(
            "/posts/comment/",
            data={"content": "comment1 content", "post": f"{self.post1.pk}"},
            HTTP_AUTHORIZATION=make_token(st1),
        )
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    def test_student_comment_get_all(self):
        wallet = Wallet.objects.create(id="sddsd1123")
        st1 = Student.objects.create(wallet=wallet)
        md.Comment.objects.create(
            content="test content", author=st1, post=self.post1, approved=True
        )
        md.Comment.objects.create(
            content="test content 2", author=st1, post=self.post1, approved=False
        )
        md.Comment.objects.create(
            content="test content 4", author=st1, post=self.post1, approved=True
        )

        comments = md.Comment.objects.filter(approved=True)
        serializer = CommentSerializer(comments, many=True)
        res = self.client.get(
            "/posts/comment/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(serializer.data, json.loads(res.content)["results"])

    def test_student_comment_get(self):
        wallet = Wallet.objects.create(id="sddsd1123")
        st1 = Student.objects.create(wallet=wallet)
        cm1 = md.Comment.objects.create(
            content="test content", author=st1, post=self.post1, approved=True
        )
        res = self.client.get(
            f"/posts/comment/{cm1.pk}/",
            HTTP_AUTHORIZATION=make_token(st1),
        )
        self.assertEqual(json.loads(res.content), CommentSerializer(cm1).data)

    def test_student_like_post(self):
        wallet = Wallet.objects.create(id="sddsd1123")
        st1 = Student.objects.create(wallet=wallet)

        res = self.client.get(
            f"/posts/like/{self.post1.pk}/",
            HTTP_AUTHORIZATION=make_token(st1),
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_student_dislike_post(self):
        wallet = Wallet.objects.create(id="sddsd1123")
        st1 = Student.objects.create(wallet=wallet)

        res = self.client.get(
            f"/posts/dislike/{self.post1.pk}/",
            HTTP_AUTHORIZATION=make_token(st1),
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
