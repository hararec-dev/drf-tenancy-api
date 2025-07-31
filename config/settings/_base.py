from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY", default="dummy-secret-key")
DEBUG = config("DEBUG", default=False, cast=bool)
APPEND_SLASH = False
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
