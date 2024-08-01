from django.urls import path
from ..views import category_views

app_name = "api-v1-blog-category"

urlpatterns = [
    path(
        "",
        category_views.CategoryViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="post-list",
    ),
    path(
        "<str:pk>/",
        category_views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="post-detail",
    ),
]
