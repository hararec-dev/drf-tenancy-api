from decouple import config

SPECTACULAR_SETTINGS = {
    "TITLE": config("SPECTACULAR_TITLE", default="Boilerplate API"),
    "DESCRIPTION": config(
        "SPECTACULAR_DESCRIPTION",
        default="API documentation for the DRF Boilerplate project",
    ),
    "VERSION": config("SPECTACULAR_VERSION", default="1.0.0"),
    "SERVE_INCLUDE_SCHEMA": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
    },
    "SECURITY": [
        {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    ],
}
