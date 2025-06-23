from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.tenancies.models import Tenant

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model. A user always belongs to a tenant.
    Corresponds to the 'users' table.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        verbose_name=_("tenant"),
        null=True,
        blank=True,
        help_text=_("The tenant the user belongs to. Null for system superadmins."),
    )
    email = models.EmailField(_("email"), max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    avatar_url = models.URLField(_("avatar URL"), max_length=255, blank=True, null=True)
    mfa_secret = models.CharField(
        _("MFA secret"), max_length=100, blank=True, null=True
    )
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(
        _("staff"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site."),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    deleted_at = models.DateTimeField(_("deleted at"), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        unique_together = [["tenant", "email"]]
        indexes = [
            models.Index(fields=["tenant"], name="idx_users_tenant_id"),
            models.Index(
                fields=["tenant", "is_active"], name="idx_users_tenant_id_is_active"
            ),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
