from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import Permission

from .middleware import get_current_tenant


class TenantRolePermissionBackend(BaseBackend):
    """
    Backend that, in addition to normal authentication, loads
    user.user_permissions based on UserTenantRole -> RolePermission.
    """

    def authenticate(self, request, user=None):
        return user

    def get_user_permissions(self, user_obj, obj=None):
        tenant = get_current_tenant()
        if not tenant or not user_obj.is_authenticated:
            return set()

        perms = Permission.objects.filter(
            rolepermission__role__usertenantrole__user=user_obj,
            rolepermission__role__usertenantrole__tenant=tenant,
        ).values_list("content_type__app_label", "codename")
        return {f"{app}.{codename}" for app, codename in perms}

    def get_group_permissions(self, user_obj, obj=None):
        return set()
