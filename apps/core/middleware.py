import logging
import time
import uuid

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("django.request")


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None:
        request_id = request.META.get("HTTP_X_REQUEST_ID", uuid.uuid4().hex)
        request.request_id = request_id  # type: ignore[attr-defined]
        request.start_time = time.time()  # type: ignore[attr-defined]
        return None

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        duration = time.time() - getattr(request, "start_time", time.time())
        ms_duration = duration * 1000

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
            "duration": ms_duration,
        }

        if settings.DEBUG:
            response["X-Request-ID"] = getattr(request, "request_id", "none")
        else:
            if response.status_code >= 400:
                response["X-Request-ID"] = getattr(request, "request_id", "none")

        if response.status_code >= 500:
            logger.error(
                f"{request.method} {request.path} → {response.status_code} ({ms_duration:.2f}ms)",
                extra=log_context,
            )
        elif response.status_code >= 400:
            logger.warning(
                f"{request.method} {request.path} → {response.status_code} ({ms_duration:.2f}ms)",
                extra=log_context,
            )
        else:
            logger.info(
                f"{request.method} {request.path} → {response.status_code} ({ms_duration:.2f}ms)",
                extra=log_context,
            )

        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> None:
        duration = time.time() - getattr(request, "start_time", time.time())
        ms_duration = duration * 1000

        log_context = {
            "user": (request.user.email if hasattr(request, "user") and request.user.is_authenticated else "anonymous"),
            "ip": request.META.get("REMOTE_ADDR", ""),
            "request_id": getattr(request, "request_id", "none"),
            "method": request.method,
            "path": request.path,
            "status_code": 500,
            "duration": ms_duration,
        }

        logger.error(
            f"UNCATCHED EXCEPTION: {type(exception).__name__} - {str(exception)}",
            exc_info=True,
            extra=log_context,
        )

        return None
