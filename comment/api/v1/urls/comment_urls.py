from django.urls import path, include
from comment.api.v1.views import comment_views

app_name = "api-v1-comment"
urlpatterns = [
    path('create/',
         comment_views.CommentCreateAPIView.as_view(),
         name='create-comment'),
    path('replay/',
         comment_views.CommentReplayCreateAPIView.as_view(),
         name='replay-profile'),
    path('<str:pk>/', comment_views.CommentViewSet.as_view(
        {'put': 'update', 'delete': 'destroy'}), name="comment-update-destroy"),
    # path('edit/',
    #      profile_views.ProfileRetrieveAPIView.as_view(),
    #      name='get-profile'),
    # path('delete/',
    #      profile_views.ProfileRetrieveAPIView.as_view(),
    #      name='get-profile'),

]
