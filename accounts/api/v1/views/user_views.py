from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers import user_serializers

User = get_user_model()


class UserRegistrationCreateAPIView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    """

    serializer_class = user_serializers.UserRegistrationSerializer
    queryset = User.objects.all()


class UserLoginGenericAPIView(generics.GenericAPIView):
    """
    Endpoint for user login. Returns authentication token on success.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = user_serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetUpdateAPIView(generics.UpdateAPIView):
    """
    Endpoint to reset  user  password .
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = user_serializers.PasswordResetSerializer
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = self.get_object()
            if user.check_password(serializer.validated_data["old_password"]):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Incorrect old password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSetPermissionsUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = user_serializers.AdminSetPermissionsSerializer
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object()
            user.permissions.append(serializer.validated_data["permission_name"])
            user.save()
            return Response(
                {"message": "User Permission updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
