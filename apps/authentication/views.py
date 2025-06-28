from decouple import config
from django.core.cache import cache
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.tenancies.serializers import TenantSerializer

from .serializers import UserLoginSerializer


class UserLoginView(APIView):
    """
    User login view.
    Receives email and password, returns JWT access and refresh tokens,
    and a list of tenants the user belongs to.
    """

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        cache_key = f"user_login:{email}:{password}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        tenants = user.get_tenants()
        tenant_serializer = TenantSerializer(tenants, many=True)

        payload = {
            "data": {
                "organizations": tenant_serializer.data,
                "accessToken": str(refresh.access_token),
                "refreshToken": str(refresh),
            },
            "meta": {
                "timestamp": now().isoformat(),
                "apiVersion": config("API_DEFAULT_VERSION", default="v1"),
            },
        }

        cache.set(cache_key, payload, config("CACHE_TIMEOUT", default=300, cast=int))
        return Response(payload, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request}
