from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin panel
    list_display = ['username', 'email', 'user_type', 'is_staff', 'is_active']

    # Define which fields should be editable in the form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

    # You can also add 'user_type' to the 'add_fieldsets' to include it in the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

    # If needed, you can define a search field to make searching by user type easier
    search_fields = UserAdmin.search_fields + ('user_type',)


# admin.site.register(models.CustomUser)
admin.site.register(models.Doctor)
admin.site.register(models.Patient)
