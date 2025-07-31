import logging
from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest
from rest_framework.response import Response


class LoggingMixin:
    """
    Mixin that provides logging functionality for ViewSets
    """

    # This attribute is expected to be set by the View that uses this mixin
    request: HttpRequest

    @property
    def logger(self) -> logging.Logger:
        logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        return logger

    def initialize_request(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpRequest:
        # The super() call is valid because this mixin is intended to be used with DRF Views.
        initialized_request = super().initialize_request(request, *args, **kwargs)  # type: ignore[misc]
        if not initialized_request:
            # In older DRF versions, initialize_request might not return a value.
            # We'll use the original request in that case.
            initialized_request = request

        self._setup_logging_context(initialized_request)
        self.logger.info(
            f"Starting request: {initialized_request.method} {initialized_request.path}",
            extra=self._get_logging_extra(initialized_request),
        )
        return initialized_request  # type: ignore[no-any-return]

    def finalize_response(self, request: HttpRequest, response: Response, *args: Any, **kwargs: Any) -> Response:
        # The super() call is valid because this mixin is intended to be used with DRF Views.
        finalized_response = super().finalize_response(request, response, *args, **kwargs)  # type: ignore[misc]
        extra = self._get_logging_extra(request)
        extra["status_code"] = finalized_response.status_code

        if finalized_response.status_code >= 500:
            self.logger.error(f"Request ended with error: {finalized_response.status_code}", extra=extra)
        elif finalized_response.status_code >= 400:
            self.logger.warning(
                f"Request ended with warning: {finalized_response.status_code}",
                extra=extra,
            )
        else:
            self.logger.info(
                f"Request completed successfully: {finalized_response.status_code}",
                extra=extra,
            )
        return finalized_response  # type: ignore[no-any-return]

    def _setup_logging_context(self, request: HttpRequest) -> None:
        """Sets up logging context for the request"""
        request.logging_context = {  # type: ignore[attr-defined]
            "user": (request.user.email if request.user.is_authenticated else "anonymous"),
            "ip": request.META.get("REMOTE_ADDR"),
            "request_id": getattr(request, "request_id", "none"),
            "method": request.method,
            "path": request.path,
        }

    def _get_logging_extra(self, request: HttpRequest) -> dict[str, Any]:
        """Gets the extra dictionary for logging"""
        return getattr(request, "logging_context", {})  # type: ignore[attr-defined]

    def log_action(self, message: str, level: str = "info", **additional_context: Any) -> None:
        """
        Method to log custom actions with additional context
        Usage in views: self.log_action("Message", level='warning', extra_field=value)
        """
        request = self.request
        extra = self._get_logging_extra(request).copy()
        extra.update(additional_context)

        log_level = level.lower()
        log_method = getattr(self.logger, log_level, self.logger.info)
        log_method(message, extra=extra)

    @classmethod
    def log_action_decorator(cls, message: str, level: str = "info") -> Callable[..., Any]:
        """
        Decorator to log the execution of a method
        Usage:
        @LoggingMixin.log_action_decorator("Creating resource")
        def create(self, request, *args, **kwargs):
        """

        def decorator(view_method: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(view_method)
            def wrapper(view: "LoggingMixin", request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
                view.log_action(f"Start: {message}", level=level, action=view_method.__name__)
                try:
                    response = view_method(view, request, *args, **kwargs)
                    view.log_action(
                        f"Completed: {message}",
                        level=level,
                        action=view_method.__name__,
                    )
                    return response
                except Exception as e:
                    view.log_action(
                        f"Error in {message}: {str(e)}",
                        level="error",
                        action=view_method.__name__,
                        exception_type=type(e).__name__,
                    )
                    raise

            return wrapper

        return decorator
