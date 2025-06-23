import logging
import uuid

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())

        logger.info(
            f"Starting request: {request.method} {request.path}",
            extra={
                "user": (
                    request.user.email
                    if hasattr(request, "user") and request.user.is_authenticated
                    else "anonymous"
                ),
                "ip": request.META.get("REMOTE_ADDR", ""),
                "request_id": request.request_id,
                "method": request.method,
                "path": request.path,
            },
        )

        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id
        return response
