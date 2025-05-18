from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.conf import settings
import yaml
from ArchiveViewer.models import Category

CONFIG_FILE = settings.CONFIG_FILE
with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "last_name",  # swapped with first_name
        "first_name",  # swapped with last_name
        "is_active",  # フィールド名を変更
        "is_staff",  # フィールド名を変更
        "is_superuser",  # フィールド名を変更
    )
    list_filter = (
        "is_superuser",  # フィールド名を変更
        "is_active",  # フィールド名を変更
        "is_staff",  # フィールド名を変更
    )
    filter_horizontal = ()
    ordering = ("email",)
    search_fields = ('email', 'last_name', 'first_name')  # swapped with last_name

    fieldsets = (
        (None, {'fields': ('email', 'last_name', 'first_name', 'password')}),  # swapped with last_name
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),  # フィールド名を変更
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')  # フィールド名を変更
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Category)

admin.site.site_header = config.get('site_title', 'Default Site Title')+ " Django管理画面"
