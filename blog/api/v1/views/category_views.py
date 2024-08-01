from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from blog.models import Category
from ..paginations import CustomPagination
from ..filters import CategoryFilters
from ..permission import CustomPermissions
from ..serializers.category_serializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermissions]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilters
    ordering_fields = ["name"]
    pagination_class = CustomPagination
    required_permission = "CategoryListCreate"
