from rest_framework import permissions

from .models import Company


class IsCompanyAdmin(permissions.BasePermission):
    message = "Must be a company administrator"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == "COMPANY"
            and Company.objects.filter(admin=request.user).exists()
        )


class IsCompanyEmployee(permissions.BasePermission):
    message = "Must be a company employee"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == "COMPANY_EMPLOYEE"
            and request.user.company is not None
        )

    def has_object_permission(self, request, view, obj):
        return obj.company == request.user.company


class IsSeller(permissions.BasePermission):
    message = "Must be a seller (individual or company)"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in [
            "SELLER_CUSTOMER",
            "INDIVIDUAL_SELLER",
            "COMPANY",
        ]


class IsAdminTech(permissions.BasePermission):
    message = "Must be a technical administrator"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "ADMIN_TECH"


class IsPrivilegedCustomer(permissions.BasePermission):
    message = "Must be a privileged customer"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.user_type == "PRIV_CUSTOMER"
        )
