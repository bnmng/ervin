from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .forms import ErvinUserCreationForm, ErvinUserChangeForm
from .models import ErvinUser, ErvinGroup
from django.contrib.auth.models import Group


class ErvinUserAdmin(UserAdmin):
    add_form = ErvinUserCreationForm
    form = ErvinUserChangeForm
    model = ErvinUser
    list_display = ["username", "email",]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("username", "password1", "password2"),},
        ),
    )


admin.site.register(ErvinUser, ErvinUserAdmin)

class ErvinGroupAdmin(GroupAdmin):
    model = ErvinGroup
    list_display = ['name', 'grp_order']

admin.site.register(ErvinGroup, ErvinGroupAdmin)

admin.site.unregister(Group)

# vim sts=4 ts=4 sw=4 et ai
