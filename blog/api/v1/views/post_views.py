from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from blog.models import Post, Category
from ..paginations import CustomPagination
from ..filters import PostFilters
from ..permission import CustomPermissions
from ..serializers.post_serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermissions]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilters
    ordering_fields = ["created_date"]
    pagination_class = CustomPagination
    required_permission = 'PostListCreate'
