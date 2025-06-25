from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseAuditModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    deleted_at = models.DateTimeField(_("deleted at"), null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
