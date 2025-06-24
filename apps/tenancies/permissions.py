from rest_framework.permissions import BasePermission

from .middleware import get_current_tenant
from .models import UserTenantRole


class IsTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        tenant = get_current_tenant()
        if not tenant:
            return False
        return UserTenantRole.objects.filter(
            user=request.user, tenant=tenant, role__name="Admin"
        ).exists()
