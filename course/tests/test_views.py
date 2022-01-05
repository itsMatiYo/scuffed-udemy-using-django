import json
from django.db.models.query_utils import Q
from rest_framework.test import APITestCase
from rest_framework import status

from course import models as md
from course.serializers import (
    CourseCopySerializer4Admin,
    CourseSerializer,
    CourseSerializer4students,
    CourseSerializerList,
)
from lapi.models import Attrib, Category
from posts_api.tests.utils import make_admin_token, make_token
from users.models import Student, Teacher, Wallet


class CourseTest(APITestCase):
    def setUp(self) -> None:
        cat1 = Category.objects.create(
            name="main par1",
            level=0,
            commission=20,
            commission_adviser=13,
            price_adviser=2,
            description="",
        )
        teacher1_wallet = Wallet.objects.create(id="test wallet id sd1233")
        self.teacher1 = Teacher.objects.create(wallet=teacher1_wallet, approved=True)

        teacher2_wallet = Wallet.objects.create(id="test wallet id sd12332")
        self.teacher2 = Teacher.objects.create(wallet=teacher2_wallet, approved=True)

        teacher3_wallet = Wallet.objects.create(id="test wallet id sd12331")
        self.student1 = Student.objects.create(wallet=teacher3_wallet)

        self.att1 = Attrib.objects.create(
            name="attrib name 1",
            category=cat1,
        )
        self.att1.teachers.add(self.teacher1)
        self.cour1 = md.Course.objects.create(
            teacher=self.teacher1,
            attrib=self.att1,
            title="course title",
            description="course 1 description",
            init_price=120,
            price=20,
            approved=True,
            duration=200,
        )
        md.Course.objects.create(
            teacher=self.teacher1,
            attrib=self.att1,
            title="course title",
            description="course 1 description",
            init_price=120,
            price=20,
            approved=False,
            duration=200,
        )
        self.course2 = md.Course.objects.create(
            teacher=self.teacher2,
            attrib=self.att1,
            title="course title",
            description="course 1 description",
            init_price=120,
            price=20,
            approved=False,
            duration=200,
        )
        self.course2.students.add(self.student1)

    def test_teacher_course_create(self):
        res = self.client.post(
            "/course/",
            data={
                "attrib": f"{self.att1.pk}",
                "title": "course title",
                "description": "course 1 description",
                "init_price": "120",
                "price": "20",
                "approved": "True",
                "duration": "200",
            },
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_course_get_all(self):
        res = self.client.get(
            "/course/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        courses = md.Course.objects.filter(Q(approved=True) | Q(teacher=self.teacher1))
        self.assertEqual(
            json.loads(res.content)["results"],
            CourseSerializerList(courses, many=True).data,
        )
        res = self.client.get("/course/")
        courses = md.Course.objects.filter(approved=True)
        self.assertEqual(
            json.loads(res.content)["results"],
            CourseSerializerList(courses, many=True).data,
        )

    def test_bought_courses_get(self):
        res = self.client.get(
            "/course/bought/",
            HTTP_AUTHORIZATION=make_token(self.student1),
        )
        courses = md.Course.objects.filter(
            teacher=self.teacher1, students__in=[self.student1]
        )
        self.assertEqual(
            json.loads(res.content)["results"],
            CourseSerializerList(courses, many=True).data,
        )

    def test_course_get(self):
        res = self.client.get(
            f"/course/{self.cour1.pk}/",
        )
        self.assertEqual(
            CourseSerializer4students(self.cour1).data, json.loads(res.content)
        )

    def test_owner_course_get(self):
        res = self.client.get(
            f"/course/owner/{self.cour1.pk}/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        self.assertEqual(json.loads(res.content), CourseSerializer(self.cour1).data)
        res = self.client.get(
            f"/course/owner/{self.cour1.pk}/",
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_like_course(self):
        res = self.client.post(
            f"/course/{self.cour1.pk}/like/",
            HTTP_AUTHORIZATION=make_token(self.student1),
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.post(
            f"/course/{self.course2.pk}/like/",
            HTTP_AUTHORIZATION=make_token(self.student1),
        )
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
        res = self.client.post(
            f"/course/{self.course2.pk}/like/",
            HTTP_AUTHORIZATION=make_token(self.student1),
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_all_copycourse(self):
        res = self.client.get(
            "/course/coursecopy/",
            HTTP_AUTHORIZATION=make_token(self.teacher1),
        )
        copycourses = md.CourseCopy.objects.filter(copy_of__teacher=self.teacher1)
        serializer = CourseCopySerializer4Admin(copycourses, many=True)
        self.assertEqual(serializer.data, json.loads(res.content)["results"])
