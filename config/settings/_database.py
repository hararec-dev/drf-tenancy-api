from decouple import config

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", cast=int),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"sslmode": "require"} if not config("DEBUG", cast=bool) else {},
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# DATABASE_ROUTERS = ['config.db_router.ReplicaRouter']
