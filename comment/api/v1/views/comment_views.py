from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotFound
from comment.models.comments import Comment
from ..serializers.comment_serializers import CommentCreateSerializer, ReplayCreateSerializer, \
    CommentUpdateDestroySerializer


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
        comment_id = self.kwargs.get('pk')
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFound('Comment not found.')

        if comment.user_profile.user != self.request.user:
            raise PermissionDenied('You do not have permission to modify this comment.')
        return comment

