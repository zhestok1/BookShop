from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

User = get_user_model()

@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('avatar', 'phone', 'bio')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('avatar', 'phone', 'bio')}),
    )
    
    list_display = ("username", "email", "phone", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")

