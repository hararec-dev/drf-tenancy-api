from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups_with_permissions(sender, **kwargs):
    group_permissions = {
        "PremiumCustomers": [
            "view_early_access_products",
            "access_special_discounts",
        ],
        "CompanyAdmins": [
            "add_company_employee",
            "remove_company_employee",
            "manage_company_products",
        ],
        "TechAdmins": [
            "view_system_metrics",
            "manage_user_accounts",
        ],
    }

    for group_name, perms in group_permissions.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        for codename in perms:
            try:
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"[WARN] Permission '{codename}' does not exist")
