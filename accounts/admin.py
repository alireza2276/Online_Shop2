from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', ]

