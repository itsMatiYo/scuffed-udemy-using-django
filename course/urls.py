from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("files", ClassFileAdminViewSet)
router.register("exam", ExamAdminViewSet)
router.register("answer", AnswerFileAdminViewSet)
router.register("seminar", SeminarAdminViewSet)
router.register("coursecopy", CourseCopyAdminViewSet)
router.register("seminarcopy", SeminarCopyAdminViewSet)
router.register("course", CourseAdminViewSet)
router.register("search", SearchObject)

urlpatterns = [
    path("admin/", include(router.urls)),
    path("<int:pk>/", CourseDetail.as_view()),
    path("<int:pk>/like/", LikeCourse.as_view()),
    path("owner/<int:pk>/", CourseDetail4Owner.as_view()),
    path("files/", ClassFileList.as_view()),
    path("files/<int:pk>/", ClassFileDetail.as_view()),
    path("exam/", ExamList.as_view()),
    path("exam/<int:pk>/", ExamDetail.as_view()),
    path("answerfile/", AnswerFileList.as_view()),
    path("answerfile/<int:pk>/", AnswerFileDetail.as_view()),
    path("seminar/", SeminarList.as_view()),
    path("seminar/my/", SeminarTeacherList.as_view()),
    path("seminar/<int:pk>/", SeminarDetail.as_view()),
    path("", CourseList.as_view()),
    path("bought/", CourseListBought.as_view()),
    path("seminarcopy/", SeminarCopyList.as_view()),
    path("seminarcopy/<int:pk>/", SeminarCopyDetail.as_view()),
    path("coursecopy/", CourseCopyList.as_view()),
    path("coursecopy/<int:pk>/", CourseCopyDetail.as_view()),
    path("seminar/search/", SearchSeminar.as_view()),
    path("course/search/", SearchCourse.as_view()),
    # * time
    path("seminar/times/", TimesLC.as_view()),
    path("seminar/times/<int:pk>/", TimesDUG.as_view()),
]
