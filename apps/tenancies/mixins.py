from typing import cast

from django.db.models.query import QuerySet
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ViewSetMixin

from .middleware import get_current_tenant


class TenantQuerysetMixin(ViewSetMixin):
    """
    Mixin to filter queryset by the current tenant and assign tenant on object creation.
    """

    def get_queryset(self) -> QuerySet:
        queryset = cast(QuerySet, super().get_queryset())
        tenant = get_current_tenant()
        if tenant is None:
            return queryset.none()
        return queryset.filter(tenant=tenant)

    def perform_create(self, serializer: Serializer) -> None:
        tenant = get_current_tenant()
        if tenant is None:
            raise RuntimeError("Cannot create object without a valid tenant")
        serializer.save(tenant=tenant)

    def perform_update(self, serializer: Serializer) -> None:
        serializer.save(tenant=get_current_tenant())
