from django.urls import path

from wallet_payment import views

urlpatterns = [

    # ! [payment]
    path('', views.Payment_All.as_view()),
    path('create/', views.Payment_Create.as_view()),
    # * Retrieve obj
    path('obj/<str:id>/', views.Payment_R.as_view()),

]
