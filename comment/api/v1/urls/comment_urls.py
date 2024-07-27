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
    path('periodic/', comment_views.PeriodicDeleteCreateAPIView.as_view(), name="periodic"),

    path('<str:pk>/', comment_views.CommentViewSet.as_view(
        {'put': 'update', 'delete': 'destroy'}), name="comment-update-destroy"),

    # path('periodic/', comment_views.PeriodicDeleteViewSet.as_view(), name="periodic"),
    # path('edit/',
    #      profile_views.ProfileRetrieveAPIView.as_view(),
    #      name='get-profile'),
    # path('delete/',
    #      profile_views.ProfileRetrieveAPIView.as_view(),
    #      name='get-profile'),

]
