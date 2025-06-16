import logging
from functools import wraps


class LoggingMixin:
    """
    Mixin that provides logging functionality for ViewSets
    """

    @property
    def logger(self):
        logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        return logger

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        self._setup_logging_context(request)
        self.logger.info(
            f"Starting request: {request.method} {request.path}",
            extra=self._get_logging_extra(request),
        )
        return request

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        extra = self._get_logging_extra(request)
        extra["status_code"] = response.status_code

        if response.status_code >= 500:
            self.logger.error(
                f"Request ended with error: {response.status_code}", extra=extra
            )
        elif response.status_code >= 400:
            self.logger.warning(
                f"Request ended with warning: {response.status_code}",
                extra=extra,
            )
        else:
            self.logger.info(
                f"Request completed successfully: {response.status_code}",
                extra=extra,
            )
        return response

    def _setup_logging_context(self, request):
        """Sets up logging context for the request"""
        request.logging_context = {
            "user": (
                request.user.email if request.user.is_authenticated else "anonymous"
            ),
            "ip": request.META.get("REMOTE_ADDR"),
            "request_id": getattr(request, "request_id", "none"),
            "method": request.method,
            "path": request.path,
        }

    def _get_logging_extra(self, request):
        """Gets the extra dictionary for logging"""
        return getattr(request, "logging_context", {})

    def log_action(self, message, level="info", **additional_context):
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
    def log_action_decorator(cls, message, level="info"):
        """
        Decorator to log the execution of a method
        Usage:
        @LoggingMixin.log_action_decorator("Creating resource")
        def create(self, request, *args, **kwargs):
        """

        def decorator(view_method):
            @wraps(view_method)
            def wrapper(view, request, *args, **kwargs):
                view.log_action(
                    f"Start: {message}", level=level, action=view_method.__name__
                )
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
