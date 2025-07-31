from typing import Any

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import (
    AbstractBaseUser,
    AnonymousUser,
    Permission,
)
from django.http import HttpRequest

from .middleware import get_current_tenant


class TenantRolePermissionBackend(BaseBackend):
    """
    Backend that, in addition to normal authentication, loads
    user.user_permissions based on UserTenantRole -> RolePermission.
    """

    def authenticate(self, request: HttpRequest | None, **kwargs: Any) -> AbstractBaseUser | None:
        return kwargs.get("user")

    def get_user_permissions(self, user_obj: AbstractBaseUser | AnonymousUser, obj: Any | None = None) -> set[str]:
        tenant = get_current_tenant()
        if not user_obj.is_authenticated:
            return set()

        perms = Permission.objects.filter(
            rolepermission__role__usertenantrole__user=user_obj,
            rolepermission__role__usertenantrole__tenant=tenant,
        ).values_list("content_type__app_label", "codename")
        return {f"{app}.{codename}" for app, codename in perms}

    def get_group_permissions(self, user_obj: AbstractBaseUser | AnonymousUser, obj: Any | None = None) -> set[str]:
        return set()
