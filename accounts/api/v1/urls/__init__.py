from django.urls import path, include

urlpatterns = [
    path('', include("accounts.api.v1.urls.user_urls")),
    path('profile/', include("accounts.api.v1.urls.profile_urls")),
]
