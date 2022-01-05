from django.urls import include, path

from wallet import views

urlpatterns = [

    # ! [wallet]
    # * All wallet obj
    path('', views.Wallet_All.as_view()),
    # * Update and Retrieve obj
    path('<str:id>/', views.Wallet.as_view()),

]
