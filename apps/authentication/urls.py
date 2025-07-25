from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserLoginView

urlpatterns = [
    path("login", UserLoginView.as_view(), name="auth_login"),
    path("refresh", TokenRefreshView.as_view(), name="auth_refresh"),
]
