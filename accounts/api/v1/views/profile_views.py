from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models.profile import Profile
from accounts.api.v1.serializers.profile_serialzers import (
    ProfileSerializer,
    SetProfileSerializer,
)
from ..paginations import CustomPagination
from ..permission import CustomPermissions
from ..filters import ProfileFilters

User = get_user_model()


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """
    Endpoint for user registration.
    """

    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            user = self.request.user.id
            return Profile.objects.get(user=user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProfileAdminListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated, CustomPermissions]
    serializer_class = ProfileSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    required_permission = "ProfileList"
    filterset_class = ProfileFilters


class SetProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetProfileSerializer

    def get_object(self):
        user = self.request.user.id
        return Profile.objects.get(user_id=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)  # Check if partial update
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
