from django.urls import path, include

app_name = 'settings'

urlpatterns = [
    path('api/v1/', include('settings.api.v1.urls'))
]
