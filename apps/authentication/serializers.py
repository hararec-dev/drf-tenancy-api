from typing import Any

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer to validate user login credentials (email and password).
    """

    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(_("Email and password are required."), code="authorization")

        request = self.context.get("request")
        user = authenticate(request=request, email=email, password=password)

        if not user:
            raise serializers.ValidationError(_("Unable to log in with provided credentials."), code="authorization")

        if not user.is_active:
            raise serializers.ValidationError(_("User account is disabled."), code="authorization")

        attrs["user"] = user
        return attrs
