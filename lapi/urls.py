from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("info", views.CompanyInfoViewSet)

urlpatterns = [
    path("category/", views.CategoryList.as_view()),
    path("category/<int:pk>/", views.CategoryDetail.as_view()),
    path("attrib/", views.AttribList.as_view()),
    path("attrib/<int:pk>/", views.AttribDetail.as_view()),
    path("user/ticket/", views.UserTicket.as_view()),
    path("media/", views.MediaList.as_view()),
    path("media/<int:pk>/", views.MediaDetail.as_view()),
    path("", include(router.urls)),
]
