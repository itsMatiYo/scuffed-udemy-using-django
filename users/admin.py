from django.contrib import admin

from users import models


@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Adviser)
class AdviserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    pass
