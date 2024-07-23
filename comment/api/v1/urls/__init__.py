from django.urls import path, include

urlpatterns = [
    path('', include("comment.api.v1.urls.comment_urls")),
]
