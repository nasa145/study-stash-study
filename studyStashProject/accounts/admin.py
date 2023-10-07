
# admin.py

from django.contrib import admin
from .models import User, UserProfile

# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified', 'plan', 'is_staff', 'is_superuser')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'password', 'email', 'is_verified', 'card_details', 'plan')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)

# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'mobile_number', 'location')
    search_fields = ('user__username', 'full_name', 'mobile_number', 'location')
    list_filter = ('location',)
