import logging

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Role
from .utils import get_group_permissions, get_permission_to_model_map

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_groups_with_permissions(sender, **kwargs):
    """
    Signal runs after each migration to create and assign
    groups (roles) and permissions.

    Each permission is associated with its corresponding model,
    covering the business logic and the provided models.
    """

    group_permissions = get_group_permissions()
    permission_to_model_map = get_permission_to_model_map()
    logger.info("Starting group and role creation/update...")

    for group_name, perm_codenames in group_permissions.items():
        group, group_created = Group.objects.get_or_create(name=group_name)
        if group_created:
            logger.info(f"Group '{group_name}' created.")

        permissions_for_group = []
        for codename in perm_codenames:
            model_class = permission_to_model_map.get(codename)
            if not model_class:
                logger.warning(
                    f"Permission '{codename}' in group '{group_name}' has no model mapped. Skipping."
                )
                continue

            try:
                content_type = ContentType.objects.get_for_model(model_class)
                permission = Permission.objects.get(
                    codename=codename, content_type=content_type
                )
                permissions_for_group.append(permission)
            except Permission.DoesNotExist:
                permission = Permission.objects.create(
                    codename=codename,
                    name=f"Can {codename.replace('_', ' ')}",
                    content_type=content_type,
                )
                permissions_for_group.append(permission)
                logger.debug(
                    f"  Permission '{codename}' created for model '{model_class._meta.model_name}'."
                )
            except Exception as e:
                logger.error(
                    f"Could not get/create permission '{codename}'. Error: {e}"
                )

        group.permissions.set(permissions_for_group)
        role, role_created = Role.objects.update_or_create(
            group=group,
            defaults={
                "group": group,
                "description": f"System role corresponding to the '{group_name}' group.",
            },
        )

        if role_created:
            logger.info(f"System Role '{group_name}' created and linked to Group.")
        else:
            logger.debug(f"System Role '{group_name}' found and updated.")

        role.permissions.set(group.permissions.all())
        logger.debug(f"  Permissions for Role '{group_name}' synchronized with Group.")

    logger.info("Finished creating/syncing groups and roles.")
