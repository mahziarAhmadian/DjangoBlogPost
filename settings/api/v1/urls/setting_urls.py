from django.urls import path, include
from settings.api.v1.views import setting_views

app_name = "api-v1-comment"
urlpatterns = [
    path('celery/', setting_views.CeleryViewSet.as_view(
        {'get': 'list'}), name="celery"),
    path('celery/<int:pk>', setting_views.CeleryViewSet.as_view(
        {'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}), name="celery"),

]
