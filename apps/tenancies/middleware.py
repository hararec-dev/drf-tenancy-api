import threading

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from apps.tenancies.models import Tenant

_thread_locals = threading.local()


def get_current_tenant() -> Tenant | None:
    return getattr(_thread_locals, "tenant", None)


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None:
        tenant_slug = request.headers.get("X-Organization-ID")
        try:
            tenant = Tenant.objects.get(slug=tenant_slug)
        except Tenant.DoesNotExist:
            tenant = None
        _thread_locals.tenant = tenant

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        if hasattr(_thread_locals, "tenant"):
            delattr(_thread_locals, "tenant")
        return response
