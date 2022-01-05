from django.db.models import Count
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import exceptions, generics, mixins, serializers, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from authentication.permission import (
    AdminPermission,
    ReadOnly,
    StudentPermission,
    TeacherPermission,
    TeacherPermissionUnApproved,
)
from authentication.utils import (
    get_my_object,
    is_it_admin,
    is_it_student,
    is_it_teacher,
)
from course.models import AnswerFile, ClassFile, Course, CourseCopy, Exam, Search, Times
from course.permissions import (
    StudentInCourse,
    StudentIsAnswerFileOwner,
    StudentIsInClassFile,
    TeacherDotCourseOwner,
    TeacherIsAnswerFileOwner,
    TeacherIsCourseOwner,
    TeacherIsTimesOwner,
)
from course.serializers import *
from course.serializers import (
    AnswerFileSerializer4Admin,
    AnswerFileSerializer4Student,
    AnswerFileSerializer4StudentPatch,
    ClassFileSerializer,
    ClassFileSerializer4Admin,
    ClassFileSerializerList,
    CourseSerializer,
    CourseSerializer4Admin,
    CourseSerializer4students,
    CourseSerializer4StudentsLiker,
    CourseSerializerCreate,
    CourseSerializerList,
    ExamSerializer4Admin,
    ExamSerializer4Teacher,
    ExamSerializerAfter,
    ExamSerializerList,
    ExamSerializerNow,
)
from users.models import Student, Teacher


# ! Course Views
class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.filter(approved=True)
    filterset_fields = (
        "price",
        "title",
        "attrib",
        "teacher",
        "approved",
    )
    permission_classes = [ReadOnly | TeacherPermission]

    def get_queryset(self):
        if is_it_teacher(self.request):
            return Course.objects.filter(
                Q(approved=True) | Q(teacher=get_my_object(self.request, Teacher))
            )
        return super().get_queryset()

    def get_serializer_class(self):
        req = self.request
        if req.method == "GET":
            return CourseSerializerList
        elif req.method == "POST":
            return CourseSerializerCreate

    def get(self, request, *args, **kwargs):
        order = request.GET.get("priceas", None)
        likes = request.GET.get("likes")
        teacher = request.GET.get("teacher")

        if order == "asc":
            self.queryset = self.queryset.order_by("price")
        elif order == "desc":
            self.queryset = self.queryset.order_by("-price")

        if teacher is not None:
            self.queryset = self.queryset.filter(teacher__wallet__id=teacher)

        if likes == "asc":
            self.queryset = self.queryset.annotate(num_likes=Count("likes")).order_by(
                "num_likes"
            )
        elif likes == "desc":
            self.queryset = self.queryset.annotate(num_likes=Count("likes")).order_by(
                "-num_likes"
            )

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = [TeacherPermission]
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        attrib = serializer.validated_data.get("attrib")
        teacher = get_my_object(request=self.request, model=Teacher)
        if attrib in teacher.attribs.all():
            return serializer.save(teacher=teacher)
        else:
            raise serializers.ValidationError({"attrib": "You don't have the attrib"})


class CourseListBought(generics.ListAPIView):
    queryset = Course.objects.filter(approved=True)
    filterset_fields = (
        "attrib",
        "price",
        "title",
        "teacher",
    )
    serializer_class = CourseSerializerList
    # Student Only
    permission_classes = [StudentPermission]

    def get(self, request, *args, **kwargs):
        student = get_my_object(request, Student)
        self.queryset = self.queryset.filter(students__in=[student])
        return self.list(request, *args, **kwargs)


class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.filter(approved=True)
    serializer_class = CourseSerializer4students


class CourseDetail4Owner(generics.RetrieveAPIView):
    permission_classes = [(TeacherPermission & TeacherIsCourseOwner)]
    serializer_class = CourseSerializer

    def get_queryset(self):
        req = self.request
        if is_it_teacher(req):
            return Course.objects.filter(teacher=get_my_object(req, Teacher))
        raise exceptions.NotFound()


class LikeCourse(APIView):
    serializer_class = CourseSerializer4StudentsLiker
    permission_classes = [StudentPermission & StudentInCourse]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except:
            raise Http404

    def post(self, request, pk, format=None):
        obj = self.get_object(pk)
        self.check_object_permissions(request, obj)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            student = get_my_object(request, Student)
            if student not in obj.likes.all():
                obj.likes.add(student)
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                obj.likes.remove(student)
                return Response(status=status.HTTP_204_NO_CONTENT)


class CourseCopyList(generics.ListCreateAPIView):
    serializer_class = CourseCopySerializer4Admin
    permission_classes = [TeacherPermission]
    filterset_fields = ("delete_request",)

    def get_queryset(self):
        return CourseCopy.objects.filter(
            copy_of__teacher=get_my_object(self.request, Teacher)
        )

    def perform_create(self, serializer):
        course = serializer.validated_data.get("copy_of")
        if course.teacher == get_my_object(self.request, Teacher):
            return serializer.save()
        else:
            raise exceptions.PermissionDenied("You cannot do this")


class CourseCopyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseCopySerializer4Admin
    permission_classes = [TeacherPermission]
    filterset_fields = ("delete_request",)

    def get_queryset(self):
        req = self.request
        if is_it_teacher(req):
            return CourseCopy.objects.filter(
                copy_of__teacher=get_my_object(req, Teacher)
            )


class SeminarCopyList(generics.ListCreateAPIView):
    serializer_class = SeminarCopySerializer4Admin
    permission_classes = [TeacherPermission]
    filterset_fields = ("delete_request",)

    def get_queryset(self):
        req = self.request
        if is_it_teacher(req):
            return SeminarCopy.objects.filter(
                copy_of__teacher=get_my_object(req, Teacher)
            )

    def perform_create(self, serializer):
        seminar = serializer.validated_data.get("copy_of")
        if seminar.teacher == get_my_object(self.request, Teacher):
            return serializer.save()
        else:
            raise exceptions.PermissionDenied("You cannot do this")


class SeminarCopyDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [TeacherPermission]
    serializer_class = SeminarCopySerializer4Admin

    def get_queryset(self):
        req = self.request
        if is_it_teacher(req):
            return SeminarCopy.objects.filter(
                copy_of__teacher=get_my_object(req, Teacher)
            )


# ! Seminars Views
class SeminarList(generics.ListCreateAPIView):
    queryset = Seminar.objects.filter(approved=True)
    permission_classes = [TeacherPermission | ReadOnly]
    filterset_fields = (
        "attrib",
        "price",
        "title",
        "teacher",
        "approved",
    )

    def get_queryset(self):
        if is_it_teacher(self.request):
            return Seminar.objects.filter(
                Q(approved=True) | Q(teacher=get_my_object(self.request, Teacher))
            )
        return self.queryset

    def get_serializer_class(self):
        req = self.request
        if req.method == "GET":
            return SeminarSerializerList
        elif req.method == "POST":
            return SeminarSerializerCreate

    def get(self, request, *args, **kwargs):
        order = request.GET.get("priceas", None)
        likes = request.GET.get("likes", None)
        teacher = request.GET.get("teacher", None)

        if order == "asc":
            self.queryset = self.queryset.order_by("price")
        elif order == "desc":
            self.queryset = self.queryset.order_by("-price")

        if teacher is not None:
            self.queryset = self.queryset.filter(teacher__wallet__id=teacher)

        if likes == "asc":
            self.queryset = self.queryset.annotate(num_likes=Count("likes")).order_by(
                "num_likes"
            )
        elif likes == "desc":
            self.queryset = self.queryset.annotate(num_likes=Count("likes")).order_by(
                "-num_likes"
            )

        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        attrib = serializer.validated_data.get("attrib")
        teacher = get_my_object(request=self.request, model=Teacher)
        if attrib in teacher.attribs.all():
            return serializer.save(teacher=teacher)
        else:
            raise serializers.ValidationError({"attrib": "You don't have the attrib"})


class SeminarTeacherList(generics.ListAPIView):
    permission_classes = [TeacherPermission]
    serializer_class = SeminarSerializer4Teacher
    filterset_fields = [
        "approved",
        "attrib",
    ]

    def get_queryset(self):
        teacher = get_my_object(self.request, Teacher)
        return Seminar.objects.filter(teacher=teacher)


class SeminarDetail(generics.RetrieveAPIView):
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer4Students
    permission_classes = []

    def get_serializer_class(self):
        pk = self.kwargs.get("pk")
        # get obj from request
        seminar = Seminar.objects.get(pk=pk)
        # get student from request
        try:
            # check if student is a in students of this semianr or not
            student = get_my_object(self.request, Student)
            if student in seminar.students.all():
                now = timezone.now()
                if now > seminar.starting_time:
                    return SeminarSerializer4BuyerStudents
            return SeminarSerializer4Students
        except:
            try:
                teacher = get_my_object(self.request, Teacher)
                if teacher == seminar.teacher:
                    return SeminarSerializer4Teacher
                return SeminarSerializer4Students
            except:
                return SeminarSerializer4Students

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# ! ClassFile Views
class ClassFileList(generics.ListCreateAPIView):
    queryset = ClassFile.objects.all()
    # add teacher to filters later
    filterset_fields = (
        "course",
        "approved",
    )
    serializer_class = ClassFileSerializerList
    # Only teacher student will use the detail one
    permission_classes = [TeacherPermission & TeacherDotCourseOwner]

    def get(self, request, *args, **kwargs):
        """filter class files for teacher"""
        self.queryset = self.queryset.filter(
            course__teacher=get_my_object(request, Teacher)
        )
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        course = serializer.validated_data.get("course")
        teacher = get_my_object(self.request, Teacher)
        if course.teacher == teacher:
            return serializer.save()
        else:
            raise serializers.ValidationError(
                {"course": "This course is not owned by this user"}
            )


class ClassFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassFile.objects.all()
    # Teacher or student particaptes in course
    permission_classes = [
        (TeacherPermission & TeacherDotCourseOwner) | (ReadOnly & StudentIsInClassFile)
    ]
    serializer_class = ClassFileSerializer

    def get(self, request, *args, **kwargs):
        """if user is student then self.queryset = filter(approved=True)"""
        if is_it_student(request):
            self.queryset = self.queryset.filter(approved=True)
            # check permission
            obj = self.get_object()
            student = get_my_object(request, Student)
            if student not in obj.course.students.all():
                raise exceptions.PermissionDenied("You cannot access this file")
        if is_it_teacher(request):
            obj = self.get_object()
            teacher = get_my_object(request, Teacher)
            if obj.course.teacher != teacher:
                raise exceptions.PermissionDenied("You cannot access this file")
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(approved=False)


# ! Exam Views
class ExamList(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    filterset_fields = ("course",)
    serializer_class = ExamSerializerList
    # [ Isteacher Or Student ]
    permission_classes = [TeacherPermission | (StudentPermission & ReadOnly)]

    def get(self, request, *args, **kwargs):
        """agar teacher bud faqat exam haye khodesh ro neshun bede
        if student:
        self.queryset.filter(course__student__in=[request.user])"""
        if is_it_teacher(request):
            self.queryset = self.queryset.filter(
                course__teacher=get_my_object(request, Teacher)
            )
        elif is_it_student(request):
            self.queryset = self.queryset.filter(
                course__students__in=[get_my_object(request, Student)], approved=True
            )
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = TeacherPermission
        self.serializer_class = ExamSerializer4Teacher
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        course = serializer.validated_data.get("course")
        teacher = get_my_object(self.request, Teacher)
        if teacher == course.teacher:
            return serializer.save()
        else:
            raise serializers.ValidationError(
                {"course": "This course is not owned by this user."}
            )


class ExamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()

    # 1- teacher is in class -> ExamSerializer4Teacher
    # 2- if student in class -> read only
    permission_classes = [
        (TeacherPermission & TeacherDotCourseOwner) | (StudentIsInClassFile & ReadOnly)
    ]
    serializer_class = ExamSerializer4Teacher

    def get_object(self):
        # get the object
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **self.kwargs)
        self.check_object_permissions(self.request, obj)
        # Lets see if user is  student
        if is_it_student(self.request):
            # limiting students access to files by checking time
            now = timezone.now()
            if now > obj.start_time and obj.end_time > now:
                self.serializer_class = ExamSerializerNow
            elif now > obj.end_time:
                self.serializer_class = ExamSerializerAfter
            else:
                self.serializer_class = ExamSerializerList
        return obj

    def get(self, request, *args, **kwargs):
        if is_it_student(request):
            self.queryset = self.queryset.filter(approved=True)
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """teacher owner of exam"""
        self.serializer_class = ExamSerializer4Teacher
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """teacher owner of exam"""
        # only teacher can delete
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(approved=False)


# ! AnswerFile Views
class AnswerFileList(generics.ListCreateAPIView):
    queryset = AnswerFile.objects.all()
    serializer_class = AnswerFileSerializer4Student
    permission_classes = [
        (TeacherIsAnswerFileOwner & TeacherPermission & ReadOnly) | (StudentPermission)
    ]
    filterset_fields = [
        "exam",
    ]
    """StudentOwner or TeacherOwnerReadonly"""

    def get(self, request, *args, **kwargs):
        if is_it_student(request):
            self.queryset = self.queryset.filter(
                student=get_my_object(request, Student)
            )
        elif is_it_teacher(request):
            self.queryset = self.queryset.filter(
                exam__course__teacher=get_my_object(request, Teacher)
            )
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        # validate if student is in course's students
        exam = serializer.validated_data.get("exam")
        student = get_my_object(self.request, Student)
        now = timezone.now()
        if student in exam.course.students.all():
            pass
        else:
            raise exceptions.ValidationError(
                {"exam": "this user cannot create asnwerfile for this exam."}
            )
        # Validate if exam is running
        if now > exam.start_time and now <= exam.end_time:
            pass
        else:
            raise exceptions.ValidationError({"exam": "You cannot do this now"})
        # validate if student has submitted answerFile before
        if AnswerFile.objects.filter(student=student, exam=exam).exists():
            answer_id = AnswerFile.objects.get(student=student, exam=exam)
            raise exceptions.ValidationError(
                {
                    "exam": "This user has submitted answerfile before for this exam",
                    "AnswerFile ID": answer_id.id,
                }
            )
        else:
            return serializer.save(student=get_my_object(self.request, Student))


class AnswerFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnswerFile.objects.all()
    permission_classes = [
        (StudentIsAnswerFileOwner & StudentPermission)
        | (TeacherPermission & TeacherIsAnswerFileOwner & ReadOnly)
    ]
    """student is the owner of this answerfile or Teacher Owner readonly"""
    serializer_class = AnswerFileSerializer4Student

    def patch(self, request, *args, **kwargs):
        self.serializer_class = AnswerFileSerializer4StudentPatch
        return self.partial_update(request, *args, **kwargs)


# ! admin ViewSets
class CourseAdminViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer4Admin
    permission_classes = [AdminPermission]
    filterset_fields = [
        "teacher",
        "attrib",
        "approved",
        "city",
    ]


class ClassFileAdminViewSet(viewsets.ModelViewSet):
    queryset = ClassFile.objects.all()
    serializer_class = ClassFileSerializer4Admin
    permission_classes = [AdminPermission]
    filterset_fields = ["course", "approved", "free"]


class ExamAdminViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer4Admin
    permission_classes = [AdminPermission]
    filterset_fields = ["course"]


class AnswerFileAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminPermission]
    queryset = AnswerFile.objects.all()
    serializer_class = AnswerFileSerializer4Admin
    filterset_fields = ["student", "exam"]


class SeminarAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminPermission]
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer4Admin
    filterset_fields = [
        "teacher",
        "attrib",
        "approved",
        "city",
    ]


class SeminarCopyAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminPermission]
    queryset = SeminarCopy.objects.all()
    serializer_class = SeminarCopySerializer4Admin
    filterset_fields = ("delete_request",)


class CourseCopyAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminPermission]
    queryset = CourseCopy.objects.all()
    serializer_class = CourseCopySerializer4Admin
    filterset_fields = ("delete_request",)


class TimesLC(generics.ListCreateAPIView):
    permission_classes = [AdminPermission | TeacherPermission]
    queryset = Times.objects.all()
    serializer_class = TimesSerializer

    def get_queryset(self):
        if is_it_teacher(self.request):
            teacher_obj = get_my_object(self.request, Teacher)
            return self.queryset.filter(seminar__teacher=teacher_obj)
        elif is_it_admin(self.request):
            return Times.objects.all()

    def perform_create(self, serializer):
        if is_it_teacher(self.request):
            teacher_obj = get_my_object(self.request, Teacher)
            seminar_obj = serializer.validated_data.get("seminar")
            if seminar_obj.teacher == teacher_obj:
                return serializer.save()
        elif is_it_admin(self.request):
            return serializer.save()
        else:
            raise exceptions.PermissionDenied("You cannot do this")


class TimesDUG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Times.objects.all()
    serializer_class = TimesSerializer
    permission_classes = [(TeacherPermission & TeacherIsTimesOwner) | AdminPermission]

    def get_queryset(self):
        if is_it_teacher(self.request):
            teacher_obj = get_my_object(self.request, Teacher)
            queryset = self.queryset
            return queryset.filter(seminar__teacher=teacher_obj)
        elif is_it_admin(self.request):
            return Times.objects.all()


class SearchSeminar(ListAPIView):
    serializer_class = SeminarSerializer4Admin
    filterset_fields = ["attrib"]

    def get_queryset(self):
        queryset = Seminar.objects.filter(approved=True)
        if self.request.GET.get("price__lt"):
            lt = self.request.GET.get("price__lt")
            queryset = queryset.filter(price__lt=lt)
        if self.request.GET.get("price__gt"):
            gt = self.request.GET.get("price__gt")
            queryset = queryset.filter(price__gt=gt)
        return queryset


class SearchCourse(ListAPIView):
    serializer_class = CourseSerializer
    filterset_fields = ["attrib"]

    def get_queryset(self):
        queryset = Course.objects.filter(approved=True)
        if self.request.GET.get("price__lt"):
            lt = self.request.GET.get("price__lt")
            queryset = queryset.filter(price__lt=lt)
        if self.request.GET.get("price__gt"):
            gt = self.request.GET.get("price__gt")
            queryset = queryset.filter(price__gt=gt)
        return queryset


class SearchObject(viewsets.ModelViewSet):
    serializer_class = SearchSerializer
    queryset = Search.objects.all()
    permission_classes = [AdminPermission | ReadOnly]
    filterset_fields = ("name",)
