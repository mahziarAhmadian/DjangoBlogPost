from django.urls import path, include

app_name = "comments"

urlpatterns = [path("api/v1/", include("comment.api.v1.urls"))]
