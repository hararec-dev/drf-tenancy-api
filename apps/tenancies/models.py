from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseAuditModel, TimestampedModel


class Tenant(BaseAuditModel):
    """
    Represents a tenant in the system. Each tenant is an isolated entity
    with its own users, organizations, and data.
    Corresponds to the 'tenants' table.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        SUSPENDED = "suspended", _("Suspended")
        DELETED = "deleted", _("Deleted")
        PENDING_SETUP = "pending_setup", _("Pending setup")
        TRIAL = "trial", _("Trial")

    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(
        _("slug"),
        max_length=100,
        unique=True,
        help_text=_("Unique URL identifier, e.g. 'my-company'"),
    )
    domain = models.CharField(
        _("domain"),
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Custom domain for the tenant"),
    )
    status = models.CharField(
        _("status"), max_length=50, choices=Status.choices, default=Status.PENDING_SETUP
    )
    parent_tenant = models.ForeignKey(
        "self",
        verbose_name=_("parent tenant"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("For hierarchical structures (resellers, etc.)"),
    )
    onboarding_completed_at = models.DateTimeField(
        _("onboarding completed at"), null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tenants"
        verbose_name = _("tenant")
        verbose_name_plural = _("tenants")
        ordering = ["name"]


class TenantConfiguration(TimestampedModel):
    """
    Specific configurations for each tenant, such as branding, localization,
    and custom settings.
    Corresponds to the 'tenant_configurations' table.
    """

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data_residency_region = models.CharField(
        _("data residency region"), max_length=50, default="us-east-1"
    )
    timezone = models.CharField(_("timezone"), max_length=50, default="UTC")
    locale = models.CharField(_("locale"), max_length=10, default="en-US")
    branding = models.JSONField(
        _("branding"),
        default=dict,
        help_text=_("Container for tenant branding."),
    )
    settings = models.JSONField(
        _("settings"),
        default=dict,
        help_text=_("Container for various tenant-specific settings."),
    )

    def __str__(self):
        return f"Configuration for {self.tenant.name}"

    class Meta:
        db_table = "tenant_configurations"
        verbose_name = _("tenant configuration")
        verbose_name_plural = _("tenant configurations")


class Role(TimestampedModel):
    """
    A set of permissions that can be assigned to users.
    Can be a system role (tenant=NULL) or a tenant-specific role.
    Corresponds to the 'roles' table.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        related_name="roles",
        help_text=_("Null for global system roles."),
    )
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True, null=True)
    permissions = models.ManyToManyField(
        Permission, through="RolePermission", verbose_name=_("permissions")
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        if self.tenant:
            return f"{self.name} ({self.tenant.name})"
        return f"{self.name} (System Role)"

    class Meta:
        db_table = "roles"
        verbose_name = _("role")
        verbose_name_plural = _("roles")
        unique_together = [["tenant", "name"]]
        indexes = [
            models.Index(fields=["tenant"], name="idx_roles_tenant_id"),
        ]


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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user")
    )
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, verbose_name=_("tenant")
    )
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, verbose_name=_("role")
    )  # PROTECT = ON DELETE RESTRICT

    class Meta:
        db_table = "user_tenant_roles"
        verbose_name = _("user role in tenant")
        verbose_name_plural = _("user roles in tenant")
        unique_together = [["user", "tenant", "role"]]
        indexes = [
            models.Index(fields=["user"], name="idx_u_user_tenant_roles_id"),
            models.Index(fields=["tenant"], name="idx_t_user_tenant_roles_id"),
        ]


class Department(BaseAuditModel):
    """
    Represents a department within a tenant.
    Corresponds to the 'departments' table.
    """

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, verbose_name=_("tenant")
    )
    parent_department = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("parent department"),
    )
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    contact_email = models.EmailField(_("contact email"), blank=True, null=True)
    legal_name = models.CharField(
        _("legal name"), max_length=200, blank=True, null=True
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    deleted_at = models.DateTimeField(_("deleted at"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "departments"
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        unique_together = [["tenant", "name"]]
        indexes = [
            models.Index(fields=["tenant"], name="idx_departments_tenant_id"),
        ]


class UserDepartmentRole(models.Model):
    """
    Intermediate table assigning a user to a department with a specific role.
    Corresponds to the 'user_department_roles' table.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user")
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
