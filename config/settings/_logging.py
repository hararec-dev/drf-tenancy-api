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
    raise ImproperlyConfigured(
        f"No se pudo crear/configurar el directorio de logs: {e}"
    )


class SafeRotatingFileHandler(RotatingFileHandler):
    """Handler que maneja errores al escribir en el archivo de log"""

    def emit(self, record):
        try:
            return super().emit(record)
        except (PermissionError, OSError) as e:
            logging.error(f"Error al escribir en el archivo de log: {e}")
            raise
            # Enviar alerta por email o servicio de monitoreo
            # También puedes usar logging.handlers.SMTPHandler para esto


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "()": SafeRotatingFileHandler,  # Usamos nuestro handler seguro
            "filename": os.path.join(LOG_DIR, "app.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "delay": True,
        },
    },
    "root": {
        "handlers": ["file"],
    },
}

if config("DEBUG", cast=bool):
    # desarrollo
    LOGGING["handlers"]["file"].update(
        {
            "level": "DEBUG",
            "formatter": "simple",
        }
    )
    LOGGING["root"]["level"] = "DEBUG"
    LOGGING["loggers"] = {
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["file"],
            "propagate": False,
        }
    }
else:
    # producción
    LOGGING["handlers"]["file"].update(
        {
            "level": "WARNING",
            "formatter": "verbose",
        }
    )
    LOGGING["root"]["level"] = "WARNING"
    LOGGING.update(
        {
            "filters": {
                "require_debug_false": {
                    "()": "django.utils.log.RequireDebugFalse",
                }
            },
            "loggers": {
                "django": {
                    "handlers": ["file"],
                    "level": "WARNING",
                    "propagate": False,
                    "filters": ["require_debug_false"],
                },
                "django.server": {
                    "handlers": ["file"],
                    "level": "ERROR",  # Solo errores para el servidor
                    "propagate": False,
                },
                "django.db.backends": {
                    "level": "ERROR",  # Solo errores de DB
                    "handlers": ["file"],
                    "propagate": False,
                },
                "django.template": {
                    "level": "ERROR",  # Solo errores de templates
                    "handlers": ["file"],
                    "propagate": False,
                },
            },
        }
    )

    LOGGING["handlers"]["file"]["encoding"] = "utf-8"
    LOGGING["handlers"]["file"]["delay"] = False
