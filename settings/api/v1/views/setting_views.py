from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from settings.api.v1.paginations import CustomPagination
from ..permission import CustomPermissions
from django_celery_beat.models import PeriodicTask
from ..serializers.setting_serializers import CelerySerializer


class CeleryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermissions]
    serializer_class = CelerySerializer
    queryset = PeriodicTask.objects.all()
    pagination_class = CustomPagination
    method_permissions = {
        "update": "UpdateCelery",
        "partial_update": "PartialUpdateCelery",
        "destroy": "DeleteCelery",
        "list": "ListCelery",
    }

    def get_permissions(self):
        # Set the required permission based on the request method
        self.required_permission = self.method_permissions.get(self.action, "Celery")

        # Call the super method to handle other permissions
        return super().get_permissions()
