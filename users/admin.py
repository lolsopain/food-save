# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_staff'
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Extra',
            {
                'fields': (
                    'phone',
                    'role'
                )
            }
        ),
    )