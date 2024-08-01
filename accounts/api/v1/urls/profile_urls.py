from django.urls import path, include

from ..views import profile_views

app_name = "api-v1-profile"
urlpatterns = [
    path("me/", profile_views.ProfileRetrieveAPIView.as_view(), name="get-profile"),
    path(
        "admin/get/list/",
        profile_views.ProfileAdminListAPIView.as_view(),
        name="get-profile",
    ),
    path("set/", profile_views.SetProfileUpdateAPIView.as_view(), name="set-profile"),
]
