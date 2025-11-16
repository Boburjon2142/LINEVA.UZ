from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Atelye ma'lumotlari",
            {
                "fields": (
                    "full_name",
                    "atelier_name",
                    "atelier_address",
                    "phone",
                    "role",
                    "avatar",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "full_name",
                    "atelier_name",
                    "atelier_address",
                    "phone",
                    "role",
                    "avatar",
                )
            },
        ),
    )
    list_display = ("username", "full_name", "atelier_name", "phone", "role")
    list_filter = ("role",)
