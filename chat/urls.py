from django.urls import path

from chat import views

urlpatterns = [

    # ! [chat]
    path('create/', views.ChatCreate.as_view()),
    path('add-user/', views.UserAdd.as_view()),
    path('upload/file/', views.FileUploade.as_view()),

]
