from django.urls import path
from comment.api.v1.views import comment_views

app_name = "api-v1-comment"
urlpatterns = [
    path(
        "create/",
        comment_views.CommentCreateAPIView.as_view(),
        name="create-comment",
    ),
    path(
        "replay/",
        comment_views.CommentReplayCreateAPIView.as_view(),
        name="replay-profile",
    ),
    path(
        "periodic/delete/",
        comment_views.PeriodicDeleteCreateAPIView.as_view(),
        name="periodic",
    ),
    path(
        "<str:pk>/",
        comment_views.CommentViewSet.as_view(
            {"put": "update", "delete": "destroy"}
        ),
        name="comment-update-destroy",
    ),
]
