BASE_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
LOCAL_APPS = [
    "apps.base",
    "apps.users",
]
THIRD_PARTY_APPS = [
    "rest_framework_simplejwt",
    "rest_framework",
    "oauth2_provider",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_PARTY_APPS
