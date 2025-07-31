from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

Company: Any = object()


class IsCompanyAdmin(permissions.BasePermission):
    message = "Must be a company administrator"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False
        return getattr(user, "user_type", None) == "COMPANY" and Company.objects.filter(admin=user).exists()


class IsCompanyEmployee(permissions.BasePermission):
    message = "Must be a company employee"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False
        return getattr(user, "user_type", None) == "COMPANY_EMPLOYEE" and getattr(user, "company", None) is not None

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        return getattr(obj, "company", None) == getattr(request.user, "company", None)


class IsSeller(permissions.BasePermission):
    message = "Must be a seller (individual or company)"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False
        return getattr(user, "user_type", None) in [
            "SELLER_CUSTOMER",
            "INDIVIDUAL_SELLER",
            "COMPANY",
        ]


class IsAdminTech(permissions.BasePermission):
    message = "Must be a technical administrator"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False
        return getattr(user, "user_type", None) == "ADMIN_TECH"


class IsPrivilegedCustomer(permissions.BasePermission):
    message = "Must be a privileged customer"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False
        return getattr(user, "user_type", None) == "PRIV_CUSTOMER"
