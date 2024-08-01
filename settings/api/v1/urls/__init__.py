from django.urls import path, include

urlpatterns = [
    path("", include("settings.api.v1.urls.setting_urls")),
]
