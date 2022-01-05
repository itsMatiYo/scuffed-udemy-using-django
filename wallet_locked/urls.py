from django.urls import path

from wallet_locked import views

urlpatterns = [

    # ! [locked]
    path('', views.Locked_All.as_view()),
    path('create/', views.Locked_Create.as_view()),
    path('unlocked/<str:id>/', views.Locked_Unlocked.as_view()),
    path('deduct-money/<str:id>/', views.Locked_Deduct_Money.as_view()),
    # * Update - Retrieve
    path('<str:id>/', views.Locked_UR.as_view()),

]
