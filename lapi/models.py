import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.fields.json import JSONField
from rest_framework.exceptions import ValidationError

from users.models import Teacher


def PictureAndVideoValidator(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".raw",
        ".mov",
        ".wmv",
        ".avi",
        ".mp4",
        ".mvp",
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError("the file is not acceptable")


class Media(models.Model):
    thumbnail = models.ImageField(null=True, blank=True)
    alt = models.CharField(max_length=300, blank=True)
    approved = models.BooleanField(default=False)
    file = models.FileField(validators=[PictureAndVideoValidator], null=True)
    seo = JSONField(null=True)
    course = models.ForeignKey(
        "course.Course",
        related_name="medias",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    seminar = models.ForeignKey(
        "course.Seminar",
        related_name="medias",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        related_name="medias",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "posts_api.Post",
        null=True,
        blank=True,
        related_name="medias",
        on_delete=models.CASCADE,
    )


class Category(models.Model):
    name = models.CharField(max_length=75)
    level = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(4), MinValueValidator(0)]
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="subs",
        blank=True,
        null=True,
    )
    # darsade teacher
    commission = models.PositiveSmallIntegerField(null=True)
    # darsade adviser
    commission_adviser = models.PositiveSmallIntegerField(null=True)
    # hazineye adviser ke tavassot e admin taeen mishavad
    price_adviser = models.PositiveBigIntegerField(null=True)
    # description
    description = models.TextField(blank=True, null=True)
    # advisers = models.ManyToManyField(
    #     'users.Adviser',
    #     related_name='categories',
    #     blank=True)
    seo = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["level"]


class Attrib(models.Model):
    name = models.CharField(max_length=75)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="attribs", null=True
    )
    teachers = models.ManyToManyField(Teacher, related_name="attribs", blank=True)

    def __str__(self) -> str:
        return f"{self.name} of {self.category}"


class Ticket4Adviser(models.Model):
    adviser = models.ForeignKey(
        "users.Adviser",
        on_delete=models.PROTECT,
        related_name="tickets",
    )
    bought_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(
        "users.Student",
        on_delete=models.DO_NOTHING,
        related_name="tickets",
    )

    class Meta:
        ordering = ["-bought_at"]


class CompanyInfo(models.Model):
    id = models.PositiveSmallIntegerField(
        default=1,
        editable=False,
        primary_key=True,
    )
    name = models.CharField(max_length=250)
    address = models.TextField()
    phonenums = models.JSONField(null=True)
    other = models.JSONField(null=True)
