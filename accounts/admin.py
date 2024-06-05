from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin class for managing CustomUser instances in the Django admin interface.

    Attributes:
        model (CustomUser): The model class that this admin class manages.
        list_display (tuple): A tuple of field names to display in the admin list view.
        list_filter (tuple): A tuple of field names to enable filtering in the admin list view.
        fieldsets (tuple): A tuple of fieldsets to organize fields in the admin detail view.
        add_fieldsets (tuple): A tuple of fieldsets for adding new CustomUser instances in the admin interface.
        search_fields (tuple): A tuple of field names to enable search functionality in the admin interface.
        ordering (tuple): A tuple of field names to specify the default ordering of CustomUser instances in the admin interface.
"""
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'bio', 'location')}),
        ('OTP Info', {'fields': ('otp_field', 'otp_created_at')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
