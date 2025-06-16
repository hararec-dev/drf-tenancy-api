from decouple import config
from pathlib import Path

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": Path(__file__).resolve().parent.parent.parent.parent
        / config("DB_NAME", default="db.sqlite3"),
    },
    #    "default": {
    #        "ENGINE": "django.db.backends.postgresql",
    #        "NAME": config("DB_NAME", "myproject"),
    #        "USER": config("DB_USER", "myuser"),
    #        "PASSWORD": config("DB_PASSWORD", "mypassword"),
    #        "HOST": config("DB_HOST", "primary-db"),
    #        "PORT": config("DB_PORT", "5432"),
    #        "CONN_MAX_AGE": 60,
    #        "OPTIONS": {"sslmode": "require"},
    #    },
    #    "replica": {
    #        "ENGINE": "django.db.backends.postgresql",
    #        "NAME": config("DB_NAME", "myproject"),
    #        "USER": config("DB_USER", "myuser"),
    #        "PASSWORD": config("DB_PASSWORD", "mypassword"),
    #        "HOST": config("DB_REPLICA_HOST", "replica-db"),
    #        "PORT": config("DB_PORT", "5432"),
    #        "CONN_MAX_AGE": 60,
    #        "OPTIONS": {"sslmode": "require"},
    #    },
}
# DATABASE_ROUTERS = ['myproject.db_router.ReplicaRouter']
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
