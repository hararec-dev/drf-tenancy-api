# CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": config("REDIS_URL", default="redis://127.0.0.1:6379/1"),
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#            "SERIALIZER": "django_redis.serializers.JSONSerializer"
#        },
#        "TIMEOUT": 300,
#    }
# }
