from rest_framework import serializers

from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tenant model, used to list tenants
    in the login response.
    """

    class Meta:
        model = Tenant
        fields = ["id", "name", "slug"]
