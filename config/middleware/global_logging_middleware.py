import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("django.request")


class GlobalLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        duration = time.time() - request.start_time

        user = "anonymous"
        if hasattr(request, "user") and request.user.is_authenticated:
            user = request.user.email

        log_context = {
            "user": user,
            "ip": request.META.get("REMOTE_ADDR", ""),
            "request_id": getattr(request, "request_id", "none"),
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration": duration * 1000,
        }

        if response.status_code >= 500:
            logger.error(
                f"{request.method} {request.path} → {response.status_code} ({duration:.2f}ms)",
                extra=log_context,
            )
        elif response.status_code >= 400:
            logger.warning(
                f"{request.method} {request.path} → {response.status_code} ({duration:.2f}ms)",
                extra=log_context,
            )
        else:
            logger.info(
                f"{request.method} {request.path} → {response.status_code} ({duration:.2f}ms)",
                extra=log_context,
            )

        return response

    def process_exception(self, request, exception):
        duration = time.time() - getattr(request, "start_time", time.time())

        log_context = {
            "user": (
                request.user.email
                if hasattr(request, "user") and request.user.is_authenticated
                else "anonymous"
            ),
            "ip": request.META.get("REMOTE_ADDR", ""),
            "request_id": getattr(request, "request_id", "none"),
            "method": request.method,
            "path": request.path,
            "status_code": 500,
            "duration": duration * 1000,
        }

        logger.error(
            f"UNCATCHED EXCEPTION: {type(exception).__name__} - {str(exception)}",
            exc_info=True,
            extra=log_context,
        )

        return None
