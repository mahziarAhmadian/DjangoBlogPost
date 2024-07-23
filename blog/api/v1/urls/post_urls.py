from django.urls import path, include
from ..views import post_views
from rest_framework.routers import DefaultRouter

app_name = "api-v1-blog"

urlpatterns = [

    path('', post_views.PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    path('<str:pk>/', post_views.PostViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="post-detail"),
]
