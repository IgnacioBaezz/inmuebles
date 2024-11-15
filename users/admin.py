from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', "is_staff"]


admin.site.register(User, CustomUserAdmin)