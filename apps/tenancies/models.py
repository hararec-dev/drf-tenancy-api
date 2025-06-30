from django.contrib.postgres.fields import ArrayField
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
    available_credits = models.DecimalField(
        _("available credits"), max_digits=12, decimal_places=2, default=0
    )
    billing_strategy = models.CharField(
        _("billing strategy"), max_length=50, default="subscription"
    )
    data_retention_policy = models.JSONField(
        _("data retention policy"), null=True, blank=True
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


class TenantAuditPolicy(models.Model):
    """
    Defines audit policies for a tenant.
    Corresponds to the 'tenant_audit_policies' table.
    """

    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_("tenant"),
    )
    log_retention_days = models.IntegerField(_("log retention days"), default=365)
    require_log_signatures = models.BooleanField(
        _("require log signatures"), default=False
    )
    sensitive_tables = ArrayField(
        models.TextField(),
        verbose_name=_("sensitive tables"),
        default=list,
        blank=True,
        help_text=_("Tables that are logged in sensitive_access_logs."),
    )

    class Meta:
        db_table = "tenant_audit_policies"
        verbose_name = _("tenant audit policy")
        verbose_name_plural = _("tenant audit policies")
