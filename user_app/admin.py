from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'role', 'password', 'is_active')}),
        ('Ruxsatlar', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muhim ma\'lumotlar', {'fields': ('last_login', 'image', 'location')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ['username', 'role', 'id', 'image', 'location', 'is_staff']
    filter_vertical = ('groups', 'user_permissions')