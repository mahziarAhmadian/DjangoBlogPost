import logging
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound
from comment.models.comments import Comment
from ..serializers.comment_serializers import (
    CommentCreateSerializer,
    ReplayCreateSerializer,
    CommentUpdateDestroySerializer,
    PeriodicDeleteSerializer,
)
from comment.task_handler import Tasks


# from django_filters.rest_framework import DjangoFilterBackend
# from ..paginations import CustomPagination
# from ..filters import CategoryFilters
# from ..permission import CustomPermissions
# from ..serializers.category_serializer import CategorySerializer


class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()


class CommentReplayCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReplayCreateSerializer
    queryset = Comment.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentUpdateDestroySerializer

    def get_object(self):
        comment_id = self.kwargs.get("pk")
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFound("Comment not found.")

        if comment.user_profile.user != self.request.user:
            raise PermissionDenied("You do not have permission to modify this comment.")
        return comment


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PeriodicDeleteCreateAPIView(generics.CreateAPIView):
    serializer_class = PeriodicDeleteSerializer

    def post(self, request, *args, **kwargs):
        logger.info("in post method")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if "date_time" in data and "task_name" in data:
                date_time = data["date_time"]
                task_name = data["task_name"]
                Tasks().crontab_schedule_delete_comments(
                    name=task_name, day_of_month=date_time.day
                )

            return Response({"status": "Task scheduled"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
