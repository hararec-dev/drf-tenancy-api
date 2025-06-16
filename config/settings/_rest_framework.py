from decouple import config

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": config("PAGE_SIZE", default=20, cast=int),
    "MAX_PAGE_SIZE": config("MAX_PAGE_SIZE", default=100, cast=int),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": config("API_DEFAULT_VERSION", default="v1"),
    "ALLOWED_VERSIONS": config(
        "API_ALLOWED_VERSIONS", default=["v1"], cast=lambda v: v.split(",")
    ),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": config("THROTTLE_RATE_ANON", default="200/day"),
        "user": config("THROTTLE_RATE_USER", default="2000/day"),
        "sensitive": config("THROTTLE_RATE_SENSITIVE", default="10/hour"),
    },
    "EXCEPTION_HANDLER": "apps.base.utils.app_exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
