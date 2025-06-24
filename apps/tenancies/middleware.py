import threading

from django.utils.deprecation import MiddlewareMixin

from apps.tenancies.models import Tenant

_thread_locals = threading.local()


def get_current_tenant():
    return getattr(_thread_locals, "tenant", None)


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tenant_slug = request.headers.get("X-Organization-ID")
        try:
            _thread_locals.tenant = Tenant.objects.get(slug=tenant_slug)
        except Tenant.DoesNotExist:
            _thread_locals.tenant = None

    def process_response(self, request, response):
        delattr(_thread_locals, "tenant")
        return response
