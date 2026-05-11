from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.services import authenticate_user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password", "confirm_password"]

    def validate(self, attrs):
        confirm_password = attrs.pop("confirm_password")
        if attrs["password"] != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs["identifier"].strip()
        password = attrs["password"]

        authenticated_user = authenticate_user(identifier=identifier, password=password)

        if not authenticated_user:
            raise serializers.ValidationError("Invalid credentials.")

        attrs["user"] = authenticated_user
        return attrs
