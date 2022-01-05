from django.db import models


class Wallet(models.Model):

    id = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return self.id


class Document(models.Model):
    file = models.FileField(null=True)
    STATUS_CHOICES = [
        ('ns', 'not seen'),
        ('ap', 'approved'),
        ('unap', 'unapproved')
    ]
    reason = models.TextField(null=True)
    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        default='ns')


class Teacher(models.Model):
    wallet = models.OneToOneField("Wallet", on_delete=models.CASCADE)
    document = models.OneToOneField(
        Document,
        on_delete=models.DO_NOTHING,
        related_name='teacher',
        null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.wallet.pk


class Student(models.Model):

    wallet = models.OneToOneField("Wallet", on_delete=models.CASCADE)

    def __str__(self):
        return self.wallet.pk


class Adviser(models.Model):
    wallet = models.OneToOneField("Wallet", on_delete=models.CASCADE)
    document = models.OneToOneField(
        Document,
        on_delete=models.DO_NOTHING,
        related_name='adviser',
        null=True,
        blank=True)
    category = models.ForeignKey(
        'lapi.Category',
        on_delete=models.DO_NOTHING,
        related_name='advisers',
        null=True,
        blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.wallet.pk
