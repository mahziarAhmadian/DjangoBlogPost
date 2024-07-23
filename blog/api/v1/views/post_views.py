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

    # Define a dictionary to map methods to permissions
    method_permissions = {
        'create': 'CreatePost',
        'update': 'UpdatePost',
        'partial_update': 'PartialUpdatePost',
        'destroy': 'DeletePost',
        'list': 'ListPosts',
        'retrieve': 'RetrievePost',
    }

    def get_permissions(self):
        # Set the required permission based on the request method
        self.required_permission = self.method_permissions.get(self.action, 'Post')

        # Call the super method to handle other permissions
        return super().get_permissions()
