from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModel
from apps.tenancies.models import Department, Tenant


class Role(TimestampedModel):
    """
    A set of permissions that can be assigned to users.
    Can be a system role (tenant=NULL) or a tenant-specific role.
    Corresponds to the 'roles' table.
    """

    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    description = models.TextField(_("description"), blank=True, null=True)
    permissions = models.ManyToManyField(
        Permission, through="RolePermission", verbose_name=_("permissions")
    )

    def __str__(self):
        return f"{self.name} (System Role)"

    class Meta:
        db_table = "roles"
        verbose_name = _("role")
        verbose_name_plural = _("roles")


class RolePermission(models.Model):
    """
    Intermediate table for the many-to-many relationship between Role and Permission.
    Corresponds to the 'role_permissions' table.
    """

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = "role_permissions"
        unique_together = [["role", "permission"]]


class UserTenantRole(models.Model):
    """
    Assigns a tenant-level role to a user (e.g., Tenant Administrator).
    Corresponds to the 'user_tenant_roles' table.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, verbose_name=_("tenant")
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name=_("role"))

    class Meta:
        db_table = "user_tenant_roles"
        verbose_name = _("user role in tenant")
        verbose_name_plural = _("user roles in tenant")
        unique_together = [["user", "tenant", "role"]]
        indexes = [
            models.Index(fields=["user"], name="idx_u_user_tenant_roles_id"),
            models.Index(fields=["tenant"], name="idx_t_user_tenant_roles_id"),
        ]


class UserDepartmentRole(models.Model):
    """
    Intermediate table assigning a user to a department with a specific role.
    Corresponds to the 'user_department_roles' table.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name=_("department")
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name=_("role"))

    class Meta:
        db_table = "user_department_roles"
        verbose_name = _("user department rol")
        verbose_name_plural = _("user department roles")
        unique_together = [
            ["user", "department", "role"],
        ]
        indexes = [
            models.Index(fields=["user"], name="idx_dept_users_user_id"),
            models.Index(fields=["department"], name="idx_dept_users_dept_id"),
        ]


class Invitation(TimestampedModel):
    """
    Stores invitations for new users to join an organization.
    Corresponds to the 'invitations' table.
    """

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACCEPTED = "accepted", _("Accepted")
        EXPIRED = "expired", _("Expired")
        REVOKED = "revoked", _("Revoked")

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, verbose_name=_("tenant")
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name=_("organization")
    )
    invited_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("invited by")
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, verbose_name=_("assigned role")
    )
    invitee_email = models.EmailField(_("invitee email"))
    token = models.CharField(_("token"), max_length=64, unique=True)
    status = models.CharField(
        _("status"), max_length=50, choices=Status.choices, default=Status.PENDING
    )
    expires_at = models.DateTimeField(_("expires at"))

    class Meta:
        db_table = "invitations"
        verbose_name = _("invitation")
        verbose_name_plural = _("invitations")
        indexes = [
            models.Index(fields=["tenant"], name="idx_invitations_tenant_id"),
            models.Index(fields=["department"], name="idx_invit_dep_id"),
        ]
