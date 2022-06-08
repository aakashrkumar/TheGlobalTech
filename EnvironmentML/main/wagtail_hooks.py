from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from .modelsData import UserProfile

INSTALLED_APPS = (
    'wagtail.contrib.styleguide',
)


class UserProfileAdmin(ModelAdmin):
    model = UserProfile
    menu_label = "User Profile"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = True
    exclude_from_explorer = False

    list_display = ("user__first_name", "user__last_name", "user__email", "avatar")
    search_fields = ("user__first_name", "user__last_name", "user__email")


class AccountModelAdminGroup(ModelAdminGroup):
    menu_label = 'Accounts'
    menu_icon = ''  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (UserProfileAdmin,)


modeladmin_register(AccountModelAdminGroup)
