import os
import logging
from decouple import config
from pathlib import Path
from logging.handlers import RotatingFileHandler
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


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "[{levelname}] {asctime} "
                "ProcessID:{process:d} ThreadID:{thread:d} "
                "Module:{module} Function:{funcName} Line:{lineno:d} "
                "User:{user} IP:{ip} "
                "RequestID:{request_id} Method:{method} Path:{path}"
                "Duration:{duration:.2f}ms "
                "Details: {message}"
            ),
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {asctime} {module}.{funcName}:{lineno} - {message}",
            "style": "{",
        },
        "request": {
            "format": (
                "[{levelname}] {asctime} "
                "RequestID:{request_id} "
                "User:{user} IP:{ip} "
                "Method:{method} Path:{path} Status:{status_code} "
                "Duration:{duration:.2f}ms "
                "Details: {message}"
            ),
            "style": "{",
        },
    },
    "filters": {
        "request_context": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: getattr(record, "request", None) is not None,
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "file": {
            "()": SafeRotatingFileHandler,
            "filename": os.path.join(LOG_DIR, "app.log"),
            "delay": True,
            "encoding": "utf-8",
        },
        "error_file": {
            "()": SafeRotatingFileHandler,
            "filename": os.path.join(LOG_DIR, "errors.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "level": "ERROR",
            "encoding": "utf-8",
        },
    },
    "root": {
        "handlers": ["file", "error_file"],
        "level": "INFO",
    },
}

if config("DEBUG", cast=bool):
    # Development configuration
    LOGGING["handlers"]["file"].update(
        {
            "level": "DEBUG",
            "formatter": "simple",
        }
    )
    LOGGING["handlers"]["error_file"].update(
        {
            "formatter": "simple",
        }
    )

    LOGGING["root"]["level"] = "DEBUG"

    LOGGING["loggers"] = {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file", "error_file"],
            "level": "WARNING",
            "propagate": False,
        },
    }
else:
    # Production configuration
    LOGGING["handlers"]["file"].update(
        {
            "level": "WARNING",
            "formatter": "verbose",
        }
    )
    LOGGING["handlers"]["error_file"].update(
        {
            "formatter": "verbose",
        }
    )

    LOGGING["root"]["level"] = "WARNING"

    LOGGING.update(
        {
            "loggers": {
                "django": {
                    "handlers": ["file", "error_file"],
                    "level": "WARNING",
                    "propagate": False,
                    "filters": ["require_debug_false"],
                },
                "django.request": {
                    "handlers": ["file", "error_file"],
                    "level": "ERROR",
                    "propagate": False,
                    "filters": ["require_debug_false"],
                },
                "django.server": {
                    "handlers": ["error_file"],
                    "level": "ERROR",
                    "propagate": False,
                },
                "django.db.backends": {
                    "handlers": ["error_file"],
                    "level": "ERROR",
                    "propagate": False,
                },
                "django.security": {
                    "handlers": ["error_file"],
                    "level": "ERROR",
                    "propagate": False,
                },
                "django.template": {
                    "handlers": ["error_file"],
                    "level": "ERROR",
                    "propagate": False,
                },
                "custom_app": {
                    "handlers": ["file", "error_file"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
        }
    )
