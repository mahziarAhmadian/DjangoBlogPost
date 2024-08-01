from django.urls import path, include

urlpatterns = [
    path("post/", include("blog.api.v1.urls.post_urls")),
    path("category/", include("blog.api.v1.urls.category_urls")),
]
