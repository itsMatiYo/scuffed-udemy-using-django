from django.contrib import admin

from course import models

admin.site.register(models.Course)
admin.site.register(models.ClassFile)
admin.site.register(models.AnswerFile)
admin.site.register(models.Exam)
admin.site.register(models.Ticket4Seminar)
admin.site.register(models.Seminar)
admin.site.register(models.Times)
