import uuid

from django.db import models

from users.models import Wallet


class DoreAmoozeshi(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    init_price = models.PositiveBigIntegerField(null=True)
    price = models.PositiveBigIntegerField()
    prequel = models.ForeignKey('self',
                                on_delete=models.CASCADE,
                                related_name='sequel',
                                blank=True,
                                null=True)
    chapters = models.TextField(blank=True)
    lessons = models.PositiveSmallIntegerField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    duration = models.PositiveBigIntegerField()  # duration by mins
    picture = models.ImageField(null=True)
    seo = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class Course(DoreAmoozeshi):
    teacher = models.ForeignKey('users.Teacher',
                                on_delete=models.PROTECT,
                                related_name='courses',
                                null=True)
    students = models.ManyToManyField('users.Student',
                                      related_name='courses',
                                      blank=True)
    waiting_students = models.ManyToManyField('users.Student',
                                              related_name='waiting_courses',
                                              blank=True)
    attrib = models.ForeignKey('lapi.Attrib',
                               on_delete=models.SET_NULL,
                               related_name='courses',
                               null=True)
    likes = models.ManyToManyField(
        'users.Student',
        related_name='like_courses',
        blank=True)


class CourseCopy(DoreAmoozeshi):
    teacher = None
    students = None
    likes = None
    attrib = models.ForeignKey('lapi.Attrib',
                               on_delete=models.SET_NULL,
                               null=True)
    copy_of = models.OneToOneField(Course,
                                   on_delete=models.CASCADE, null=True, )

    delete_request = models.BooleanField(default=False)


class Seminar(DoreAmoozeshi):
    teacher = models.ForeignKey(
        'users.Teacher',
        on_delete=models.PROTECT,
        related_name='seminars',
        null=True)
    students = models.ManyToManyField(
        'users.Student',
        related_name='seminars',
        blank=True)
    waiting_students = models.ManyToManyField('users.Student',
                                              related_name='waiting_seminars',
                                              blank=True)
    attrib = models.ForeignKey(
        'lapi.Attrib',
        on_delete=models.SET_NULL,
        related_name='seminars',
        null=True)
    likes = models.ManyToManyField(
        'users.Student',
        related_name='like_seminars',
        blank=True)
    # zarfiat e class
    capacity = models.PositiveSmallIntegerField()
    # zaman e shuru class
    starting_time = models.DateTimeField()
    # zaman e start e class
    starting_seminar = models.DateTimeField(null=True)
    # zaman e payan class
    ending_time = models.DateTimeField()
    # city
    city = models.CharField(max_length=140, null=True)
    # makane class
    place = models.CharField(max_length=300, blank=True)
    # zaman haye class
    # class_times = models.TextField()


class SeminarCopy(DoreAmoozeshi):
    teacher = None
    students = None
    attrib = models.ForeignKey(
        'lapi.Attrib',
        on_delete=models.SET_NULL,
        null=True)
    likes = None
    attrib = models.ForeignKey(
        'lapi.Attrib',
        on_delete=models.SET_NULL,
        null=True)
    # zarfiat e class
    capacity = models.PositiveSmallIntegerField()
    # zaman e shuru class
    starting_time = models.DateTimeField()
    # zaman e start e class
    starting_seminar = models.DateTimeField()
    # zaman e payan class
    ending_time = models.DateTimeField()
    # city
    city = models.CharField(max_length=140, null=True)
    # makane class
    place = models.CharField(max_length=300, blank=True)
    # zaman haye class
    class_times = models.TextField()
    copy_of = models.OneToOneField(Seminar,
                                   on_delete=models.CASCADE, related_name='copy', null=True)
    delete_request = models.BooleanField(default=False)


class Ticket4Seminar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    course = models.ForeignKey(Seminar, on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    part_id = models.CharField(max_length=100, null=True)


class ClassFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(blank=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='files')
    approved = models.BooleanField(default=False)
    free = models.BooleanField(default=False)
    seo = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['course']

    def __str__(self) -> str:
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=120, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='exams')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    question_file = models.FileField(blank=True, null=True)
    answer_file = models.FileField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_time']

    def __str__(self) -> str:
        return self.name or str(self.id)


class AnswerFile(models.Model):
    student = models.ForeignKey(
        'users.Student',
        on_delete=models.CASCADE,
        related_name='answerfiles',
        null=True)
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='answers')
    submitting_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)
    file = models.FileField(blank=True)


class Times(models.Model):
    DAY_CHOICES = [
        ('0', 'شنبه'),
        ('1', 'یک شنبه'),
        ('2', 'دو شنبه'),
        ('3', 'سه شنبه'),
        ('4', 'چهار شنبه'),
        ('5', 'پنج شنبه'),
        ('6', 'جمعه'),
    ]
    seminar = models.ForeignKey(
        Seminar, on_delete=models.CASCADE, related_name='class_times')
    start = models.TimeField(max_length=24)
    end = models.TimeField(max_length=24)
    day = models.CharField(max_length=1, choices=DAY_CHOICES)


class Search(models.Model):
    name = models.CharField(max_length=2048)
    url = models.URLField()
