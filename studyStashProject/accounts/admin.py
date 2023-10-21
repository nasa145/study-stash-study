

from django.contrib import admin
from .models import ApplicationUser, UserProfile

# Register the User model
@admin.register(ApplicationUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'plan', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'password', 'email',  'plan')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)

# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name', 'last_name', 'mobile_number', 'location')
    search_fields = ('user__username','first_name', 'last_name', 'mobile_number', 'location')
    list_filter = ('location',)
