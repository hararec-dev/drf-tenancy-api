import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from decouple import config
from django.core.exceptions import ImproperlyConfigured

BASE_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_ROOT / "logs"

try:
    os.makedirs(LOG_DIR, exist_ok=True)
    os.chmod(LOG_DIR, 0o755)
except OSError as e:
    raise ImproperlyConfigured(f"Could not create/configure the logs directory: {e}")


class SafeRotatingFileHandler(RotatingFileHandler):
    """Handler that handles errors when writing to the log file"""

    def emit(self, record):
        try:
            return super().emit(record)
        except (PermissionError, OSError) as e:
            st_mode = oct(os.stat(self.baseFilename).st_mode)
            exists = os.path.exists(self.baseFilename)
            error_msg = (
                f"Failed to write to log file '{self.baseFilename}': "
                f"Error type: {type(e).__name__}, "
                f"Description: {e.strerror}, "
                f"Error code: {e.errno}, "
                f"File permissions: {st_mode if exists else 'File does not exist'}"
            )
            logging.error(error_msg)
            raise


class SafeFormatter(logging.Formatter):
    def format(self, record):
        try:
            return super().format(record)
        except KeyError as e:
            missing_key = e.args[0]
            record.__dict__[missing_key] = f"!MISSING_{missing_key}!"
            return super().format(record)


LOGGING = {
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
                "RequestID:{request_id} Method:{method} Path:{path} "
                "Status:{status_code} Duration:{duration:.2f}ms "
                "Details: {message}"
            ),
            "style": "{",
        },
        "simple": {
            "()": SafeFormatter,
            "format": "[{levelname}] {asctime} {module}.{funcName}:{lineno} - {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "file": {
            "()": SafeRotatingFileHandler,
            "filename": LOG_DIR / "app.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
        "error_file": {
            "()": SafeRotatingFileHandler,
            "filename": LOG_DIR / "errors.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },
    "root": {
        "handlers": ["file", "error_file"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

if config("DEBUG", cast=bool):
    # Development
    LOGGING["handlers"]["file"].update(
        {
            "level": "DEBUG",
            "formatter": "simple",
        }
    )
    LOGGING["handlers"]["error_file"].update(
        {
            "level": "ERROR",
            "formatter": "simple",
        }
    )
    LOGGING["root"]["level"] = "DEBUG"
else:
    # Production
    LOGGING["handlers"]["file"].update(
        {
            "level": "WARNING",
            "formatter": "verbose",
        }
    )
    LOGGING["handlers"]["error_file"].update(
        {
            "level": "ERROR",
            "formatter": "verbose",
        }
    )
    LOGGING["loggers"]["django.request"]["filters"] = ["require_debug_false"]
