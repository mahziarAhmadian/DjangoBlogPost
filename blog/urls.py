from django.urls import path, include

app_name = "blogs"

urlpatterns = [path("api/v1/", include("blog.api.v1.urls"))]
