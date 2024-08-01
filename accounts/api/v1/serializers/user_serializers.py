from django.conf import settings
from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        required=True,
    )

    password = serializers.CharField(
        required=True,
    )

    password_2 = serializers.CharField(read_only=True)

    class Meta(object):
        model = User
        fields = ["phone_number", "password", "password_2"]

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("phone_number already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, "PASSWORD_MIN_LENGTH", 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long."
                % getattr(settings, "PASSWORD_MIN_LENGTH", 8)
            )
        return value

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get("password")
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def create(self, validated_data):

        validated_data = {
            "phone_number": validated_data.get("phone_number"),
            "password": validated_data.get("password"),
        }
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        required=True,
    )

    access = serializers.CharField(allow_blank=True, read_only=True)

    refresh = serializers.CharField(allow_blank=True, read_only=True)

    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
    permissions = serializers.JSONField(read_only=True)

    class Meta(object):
        model = User
        fields = [
            "phone_number",
            "password",
            "access",
            "refresh",
            "permissions",
        ]

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def validate(self, data):
        phone_number = data.get("phone_number", None)
        username = data.get("username", None)
        password = data.get("password", None)

        if not phone_number and not username:
            raise serializers.ValidationError(
                "Please enter username or phone_number to login."
            )

        user = (
            User.objects.filter(phone_number=phone_number)
            .exclude(phone_number__isnull=True)
            .exclude(phone_number__iexact="")
            .distinct()
        )

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError(
                "This username/phone_number is not valid."
            )

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            token = self.get_tokens_for_user(user=user_obj)
            data["access"] = token.get("access")
            data["refresh"] = token.get("refresh")
            data["permissions"] = user_obj.permissions
        else:
            raise serializers.ValidationError("User not active.")
        return data


class PasswordResetSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]


class AdminSetPermissionsSerializer(serializers.ModelSerializer):
    permission_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["permission_name"]
