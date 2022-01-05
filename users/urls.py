from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register("tickets", views.AdminTicketViewSet)
router.register("adviser", views.AdminAdviserViewset)
router.register("teacher", views.AdminTeacherViewset)
router.register("student", views.AdminStudentViewSet)
router.register("document", views.AdminDocumentViewSet)

urlpatterns = [
    # router urls
    path("admin/", include(router.urls)),
    # * student buy class
    path("buy/seminar/<int:class_id>/", views.Buy_Seminar.as_view()),
    path("seminar/accept/student/<str:student_uuid>/", views.Accept_Seminar.as_view()),
    path("buy/class/<int:class_id>/", views.Buy_Class.as_view()),
    path("buy/adviser/<int:adviser_id>/", views.Buy_Adviser.as_view()),
    # ! type ==> [giftcard , creditcard]
    path(
        "buy/class/card/<str:cart_id>/<str:type>/<int:class_id>/",
        views.Buy_Class_With_Card.as_view(),
    ),
    path(
        "buy/adviser/card/<str:cart_id>/<str:type>/<int:adviser_id>/",
        views.Buy_Adviser_With_Card.as_view(),
    ),
    path("<str:type>/document/", views.User_Create_Document.as_view()),
    path("<str:type>/update/document/", views.User_Update_Document.as_view()),
    # tickets
    path("student/tickets/", views.StudentTicketList.as_view()),
    path("adviser/tickets/", views.AdviserTicketList.as_view()),
]
