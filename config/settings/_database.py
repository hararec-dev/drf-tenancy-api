from decouple import config

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="dummy_db"),
        "USER": config("DB_USER", default="dummy_user"),
        "PASSWORD": config("DB_PASSWORD", default="dummy_password"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default=5432, cast=int),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"sslmode": "require"} if not config("DEBUG", default=False, cast=bool) else {},
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# DATABASE_ROUTERS = ['config.db_router.ReplicaRouter']
