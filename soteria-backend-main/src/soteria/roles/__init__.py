from django.conf import settings

from .helper import load_roles_config_file
from .manager import RoleManager

default_roles_config = load_roles_config_file(settings.ORGANIZATION_MEMBER_ROLES_CONFIG_FILE)
default_manager = RoleManager(
    default_roles_config,
    settings.ORGANIZATION_MEMBER_DEFAULT_ROLE,
)

can_manage = default_manager.can_manage
get = default_manager.get
get_by_name = default_manager.get_by_name
get_all = default_manager.get_all
get_choices = default_manager.get_choices
get_default = default_manager.get_default
get_top_dog = default_manager.get_top_dog
get_global_roles = default_manager.get_global_roles
get_public_info_list = default_manager.get_public_info_list
with_permission = default_manager.with_permission
get_permission_list = default_manager.get_permission_list
