from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "role",
    ]
    list_filter = ["email", "is_staff", "is_active", "role"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["email"]