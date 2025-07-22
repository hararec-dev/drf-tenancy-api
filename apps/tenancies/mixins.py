from rest_framework.viewsets import ViewSetMixin

from .middleware import get_current_tenant


class TenantQuerysetMixin(ViewSetMixin):
    """
    Mixin to filter queryset by the current tenant and assign tenant on object creation.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = get_current_tenant()
        if tenant is None:
            return queryset.none()
        return queryset.filter(tenant=tenant)

    def perform_create(self, serializer):
        tenant = get_current_tenant()
        if tenant is None:
            raise RuntimeError("Cannot create object without a valid tenant")
        serializer.save(tenant=tenant)

    def perform_update(self, serializer):
        serializer.save(tenant=get_current_tenant())
