from rest_framework import serializers
from accounts.models.profile import Profile
from accounts.models.users import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'is_superuser', 'is_staff', 'is_active', 'created_date']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'image', 'description', 'created_date', 'user']


class SetProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'description']
