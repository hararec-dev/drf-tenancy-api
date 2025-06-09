from django.db import models
from django.utils import timezone

class BaseAuditModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
