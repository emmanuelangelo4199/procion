from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'name', 'is_staff', 'is_active')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'password1', 'password2')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
