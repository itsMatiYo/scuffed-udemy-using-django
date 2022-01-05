from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet)
router.register('postcopy', views.PostCopyViewSet)
router.register('comment', views.CommentViewSet)

urlpatterns = [
    path('copy/<int:pk>/', views.PostCopyDetail.as_view()),
    path('copy/', views.PostCopyList.as_view()),
    path('comment/<int:pk>/', views.CommentDetail.as_view()),
    path('comment/', views.CommentList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('like/<int:id>/', views.PostLike.as_view()),
    path('dislike/<int:id>/', views.PostDisLike.as_view()),
    path('admin/', include(router.urls)),
    path('', views.PostList.as_view()),
]
