from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BankAccount
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = [
        "account_number",
        "user",
        "currency",
        "account_type",
        "account_balance",
        "account_status",
    ]
    list_filter = [
        "currency",
        "account_type",
        "account_status",
    ]
    search_fields = [
        "account_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    readonly_fields = ["account_number", "created_at", "updated_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "account_number",
                    "account_balance",
                    "currency",
                    "account_type",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "account_status",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

  
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return request.user.is_superuser 