from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.authentication.models import UserTenantRole

from .middleware import get_current_tenant


class IsTenantAdmin(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        tenant = get_current_tenant()
        if not tenant:
            return False
        if not request.user.is_authenticated:
            return False
        return UserTenantRole.objects.filter(user=request.user, tenant=tenant, role__group__name="TenantAdmin").exists()
