from datetime import timedelta

from decouple import Csv, config

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "config.middleware.logging_middleware.RequestLoggingMiddleware",
    "config.middleware.global_logging_middleware.GlobalLoggingMiddleware",
]
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("ACCESS_TOKEN_LIFETIME", default=5, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("REFRESH_TOKEN_LIFETIME", default=1, cast=int)
    ),
    "SIGNING_KEY": config("JWT_SIGNING_KEY"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "ALGORITHM": "HS256",
}
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config(
    "SECURE_CONTENT_TYPE_NOSNIFF", default=True, cast=bool
)
SECURE_BROWSER_XSS_FILTER = config("SECURE_BROWSER_XSS_FILTER", default=True, cast=bool)
X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default="DENY")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())
CORS_ALLOW_ALL_ORIGINS = True
