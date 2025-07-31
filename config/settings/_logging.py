import logging
import os
from pathlib import Path
from typing import Any

from decouple import config
from django.core.exceptions import ImproperlyConfigured

from config.loggers.loggers import (
    MaxLevelFilter,
    SafeFormatter,
    SafeRotatingFileHandler,
)

BASE_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_ROOT / "logs"

try:
    os.makedirs(LOG_DIR, exist_ok=True)
    os.chmod(LOG_DIR, 0o755)
except OSError as e:
    raise ImproperlyConfigured(f"Could not create/configure the logs directory: {e}")


LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": SafeFormatter,
            "format": (
                "[{levelname}] {asctime} "
                "ProcessID:{process:d} ThreadID:{thread:d} "
                "Module:{module} Function:{funcName} Line:{lineno:d} "
                "User:{user} IP:{ip} "
                "X-Request-ID:{request_id} Method:{method} Path:{path} "
                "Status:{status_code} Duration:{duration:.2f}ms "
                "Details: {message}"
            ),
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "below_error": {
            "()": MaxLevelFilter,
            "max_level": logging.ERROR,
        },
    },
    "handlers": {
        "file": {
            "()": SafeRotatingFileHandler,
            "backupCount": 5,
            "encoding": "utf-8",
            "filename": LOG_DIR / "app.log",
            "formatter": "verbose",
            "level": "DEBUG",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "filters": ["below_error"],
        },
        "error_file": {
            "()": SafeRotatingFileHandler,
            "backupCount": 5,
            "encoding": "utf-8",
            "filename": LOG_DIR / "errors.log",
            "formatter": "verbose",
            "level": "ERROR",
            "maxBytes": 1024 * 1024 * 5,
        },
    },
    "root": {
        "handlers": ["file", "error_file"],
        "level": "DEBUG",
    },
    "loggers": {
        "django.request": {
            "handlers": ["file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "apps": {
            "handlers": ["file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

if config("DEBUG", default=False, cast=bool):
    # Development
    LOGGING["handlers"].update(
        {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
        }
    )
    LOGGING["loggers"]["django.request"]["handlers"].append("console")
    LOGGING["loggers"]["apps"]["handlers"].append("console")
else:
    # Production
    LOGGING["handlers"]["file"].update(
        {
            "level": "WARNING",
        }
    )
    LOGGING["loggers"]["django.request"]["filters"] = ["require_debug_false"]
    LOGGING["loggers"]["apps"]["filters"] = ["require_debug_false"]
