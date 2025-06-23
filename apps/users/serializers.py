from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
    user_permissions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "date_joined",
            "updated_at",
            "groups",
            "user_permissions",
        )
        read_only_fields = (
            "date_joined",
            "updated_at",
            "is_staff",
            "is_active",
            "user_permissions",
            "groups",
        )
