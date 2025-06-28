from decouple import config

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('REDIS_HOST')}:{config('REDIS_PORT', cast=int)}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "PASSWORD": config("REDIS_PASSWORD"),
            "CONNECTION_POOL_KWARGS": {
                "max_connections": config(
                    "CACHE_MAX_CONNECTIONS", default=100, cast=int
                )
            },
            "SOCKET_CONNECT_TIMEOUT": config(
                "CACHE_SOCKET_CONNECT_TIMEOUT", default=5, cast=int
            ),
            "SOCKET_TIMEOUT": config("CACHE_SOCKET_TIMEOUT", default=5, cast=int),
        },
        "KEY_PREFIX": config("CACHE_KEY_PREFIX", default="api"),
        "TIMEOUT": config("CACHE_TIMEOUT", default=300, cast=int),
    },
}
