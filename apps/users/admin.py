from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel


class CustomUserAdmin(UserAdmin):
    model = UserModel
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address', 'pincode')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(UserModel)
