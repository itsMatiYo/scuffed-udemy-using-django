from django.db import models
from django.db.models.fields import TextField


class Post(models.Model):
    thumbnail = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = TextField()
    author = models.ForeignKey(
        "users.Teacher",
        related_name="posts",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("users.Student", blank=True)
    approved = models.BooleanField(default=False)
    seo = models.JSONField(blank=True, null=True)


class PostCopy(models.Model):
    thumbnail = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=250)
    content = TextField()
    post = models.OneToOneField(
        Post,
        null=True,
        blank=True,
        related_name="post_copy",
        on_delete=models.CASCADE,
    )
    delete_request = models.BooleanField(default=False)


class Comment(models.Model):
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.DO_NOTHING
    )
    author = models.ForeignKey("users.Student", null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name="comments", null=True, on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)
    seo = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = [
            "-created_at",
        ]
