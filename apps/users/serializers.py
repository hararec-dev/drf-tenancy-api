from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
        ]
        read_only_fields = [
            "id",
            "fullName",
        ]
