from django_filters import rest_framework as filters
from ...models import Post, Category


class PostFilters(filters.FilterSet):
    """
    valid filter fields arg : exact,iexact,contains,icontains,in,gt,gte,lt,lte,startswith,istartswith,endswith

    """

    class Meta:
        model = Post
        fields = {"category": ["exact"], "author": ["exact"], "status": ["exact"]}


class CategoryFilters(filters.FilterSet):
    """
    valid filter fields arg : exact,iexact,contains,icontains,in,gt,gte,lt,lte,startswith,istartswith,endswith

    """

    class Meta:
        model = Category
        fields = {"name": ["in"]}
