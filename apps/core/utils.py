import logging
from typing import Any

from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def app_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    response = exception_handler(exc, context)

    status_code = response.status_code if response is not None else status.HTTP_500_INTERNAL_SERVER_ERROR

    STATUS_CODE_MESSAGES = {
        400: "Bad request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Resource not found",
        405: "Method not allowed",
        409: "Conflict",
        429: "Too many requests",
        500: "Internal server error",
    }

    error_data = {
        "error": {
            "status": status_code,
            "message": STATUS_CODE_MESSAGES.get(status_code, "Request error"),
            "type": exc.__class__.__name__,
        }
    }

    if isinstance(exc, ValidationError):
        error_data["error"].update(
            {
                "message": "Validation error in input data",
                "details": _simplify_validation_errors(exc),
            }
        )
    elif isinstance(exc, Http404):
        error_data["error"].update({"message": "Requested resource does not exist"})
    elif response is not None and status_code < 500:
        if isinstance(response.data, dict):
            if "detail" in response.data:
                error_data["error"]["details"] = str(response.data["detail"])
            else:
                flat_messages = []
                for key, value in response.data.items():
                    if isinstance(value, list) and value:
                        flat_messages.append(f"{key}: {str(value[0])}")
                    elif isinstance(value, dict):
                        inner = ", ".join(f"{k}: {v}" for k, v in value.items())
                        flat_messages.append(f"{key}: {inner}")
                    else:
                        flat_messages.append(f"{key}: {str(value)}")
                error_data["error"]["details"] = " | ".join(flat_messages)

    _log_error_safely(exc, context, status_code)

    return Response(error_data, status=status_code, headers={"Content-Type": "application/json"})


def _simplify_validation_errors(exc: ValidationError) -> dict[str, Any] | str:
    """Simplifies validation errors to avoid exposing internal structure"""
    if hasattr(exc, "message_dict"):
        return {k: str(v[0]) for k, v in exc.message_dict.items()}
    elif hasattr(exc, "messages"):
        return {"non_field_errors": [str(msg) for msg in exc.messages]}
    return str(exc)


def _log_error_safely(exc: Exception, context: dict[str, Any], status_code: int) -> None:
    """Logs errors without exposing sensitive information"""
    request = context.get("request")
    log_data = {
        "exception_type": exc.__class__.__name__,
        "status_code": status_code,
        "view": context.get("view").__class__.__name__ if context.get("view") else None,
        "request_method": request.method if request else None,
    }

    if status_code >= 500:
        logger.error("Server error occurred", extra=log_data)
    elif status_code >= 400:
        logger.warning("Client error occurred", extra=log_data)
