from django.urls import path

from wallet_part import views

urlpatterns = [

    # ! [part]
    path('', views.Part_All.as_view()),
    # * Update - Delete - Retrieve
    path('<str:id>/', views.Part_UDR.as_view()),

]
