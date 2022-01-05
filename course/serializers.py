from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from course.models import (AnswerFile, ClassFile, Course, CourseCopy,
                           DoreAmoozeshi, Exam, Search, Seminar, SeminarCopy,
                           Times)
from users import serializers as sz


# !classFile Serializers
class ClassFileSerializerList(ModelSerializer):
    class Meta:
        model = ClassFile
        fields = ('id', 'name', 'course', 'approved',)
        read_only_fields = ('approved',)


class ClassFileSerializer(ModelSerializer):
    class Meta:
        model = ClassFile
        fields = '__all__'
        read_only_fields = ('approved',)


class TimesSerializer(ModelSerializer):
    class Meta:
        model = Times
        fields = '__all__'


# ! Course Serializers
# Serializer 4 teacher and Student(read-only)


class CourseSerializer(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    files = ClassFileSerializerList(many=True, read_only=True)
    exams = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    teacher = sz.TeacherCategoryPatch(read_only=True)
    students = sz.StudentSerializer(read_only=True, many=True)
    likes = sz.StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('approved',
                            'teacher', 'students', 'waiting_students')


class CourseSerializer4students(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    files = ClassFileSerializerList(many=True, read_only=True)
    exams = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    teacher = sz.TeacherCategoryPatch(read_only=True)
    likes = sz.StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        exclude = ('students', 'waiting_students')


class CourseSerializer4StudentsLiker(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'likes',)


class CourseSerializerCreate(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Course
        exclude = ('students', 'waiting_students',)
        read_only_fields = ('approved', 'likes',)


class CourseSerializerList(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    teacher = sz.TeacherCategoryPatch(read_only=True)
    likes = sz.StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        exclude = ('waiting_students', 'students',)


# ! Seminar Seralizers
class SeminarSerializerList(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    likes = serializers.IntegerField(source='likes.count')

    class Meta:
        model = Seminar
        exclude = ('approved', 'students', 'waiting_students',)


class SeminarSerializerCreate(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Seminar
        exclude = ('students', 'waiting_students',)
        read_only_fields = ('approved', 'likes',)
        extra_kwargs = {
            'starting_seminar': {'required': True}
        }

    def validate(self, attrs):
        starting_time = attrs.get('starting_time')
        ending_time = attrs.get('ending_time')
        if starting_time > ending_time:
            raise serializers.ValidationError(
                'start date and end date don\'t match')

        else:
            return attrs


class SeminarSerializer4Students(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    likes = sz.StudentSerializer()
    teacher = sz.TeacherCategoryPatch(read_only=True)
    students = sz.StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Seminar
        exclude = ('students', 'place', 'waiting_students')


class SeminarSerializer4BuyerStudents(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class_times = TimesSerializer(read_only=True, many=True)
    likes = sz.StudentSerializer()
    teacher = sz.TeacherCategoryPatch(read_only=True)
    students = sz.StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Seminar
        exclude = ('students', 'waiting_students')


class SeminarSerializer4Teacher(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class_times = TimesSerializer(read_only=True, many=True)
    likes = sz.StudentSerializer()
    teacher = sz.TeacherCategoryPatch(read_only=True)
    students = sz.StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Seminar
        fields = '__all__'


class SeminarSerializer4Admin(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class_times = TimesSerializer(read_only=True, many=True)
    likes = sz.StudentSerializer()
    teacher = sz.TeacherCategoryPatch()
    students = sz.StudentSerializer(many=True)
    waiting_students = sz.StudentSerializer(many=True)

    class Meta:
        model = Seminar
        fields = '__all__'


class SeminarCopySerializer4Admin(ModelSerializer):
    class Meta:
        model = SeminarCopy
        fields = '__all__'


class CourseCopySerializer4Admin(ModelSerializer):
    class Meta:
        model = CourseCopy
        fields = '__all__'


# ! Exam Serializers
class ExamSerializerList(ModelSerializer):
    class Meta:
        model = Exam
        exclude = ('question_file', 'answer_file', 'approved')


class ExamSerializerNow(ModelSerializer):
    class Meta:
        model = Exam
        exclude = ('answer_file',)


class ExamSerializerAfter(ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamSerializer4Teacher(ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ('approved',)

    def validate(self, attrs):
        # check if start time is sooner than endtime
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        if end_time > start_time:
            return attrs
        else:
            raise serializers.ValidationError(
                'Start time and end time do not match.')


# ! Answer file Serializers
class AnswerFileSerializer4Student(ModelSerializer):
    student = sz.StudentSerializer(read_only=True)

    class Meta:
        model = AnswerFile
        fields = ('id', 'exam', 'file', 'submitting_time', 'student')
        read_only_fields = ('submitting_time', 'student')

    def validate(self, attrs):
        """check if student can particpate in this exam and
        can only create one answerFile for exam"""
        return super().validate(attrs)


class AnswerFileSerializer4StudentPatch(ModelSerializer):
    student = sz.StudentSerializer(read_only=True)

    class Meta:
        model = AnswerFile
        fields = ('id', 'exam', 'file', 'submitting_time', 'student')
        read_only_fields = ('submitting_time', 'student', 'exam',)


# 4Admin Serializers
class CourseSerializer4Admin(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    exams = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    teacher = sz.TeacherCategoryPatch(read_only=True)
    students = sz.StudentSerializer(many=True)
    waiting_students = sz.StudentSerializer(many=True)
    likes = sz.StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class ClassFileSerializer4Admin(ModelSerializer):
    course = CourseSerializerList(read_only=True)

    class Meta:
        model = ClassFile
        fields = '__all__'


class ExamSerializer4Admin(ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        if end_time > start_time:
            return attrs
        else:
            raise serializers.ValidationError(
                'Start time and end time do not match.')


class AnswerFileSerializer4Admin(ModelSerializer):
    class Meta:
        model = AnswerFile
        fields = '__all__'


class SearchSerializer(ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
