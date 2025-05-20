from django.contrib import admin
from cloudinary.forms import CloudinaryFileField
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _



from .models import Profile


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = [
        "user",
        "full_name",
        "phone_number",
        "email",
        "employment_status",
    ]
    list_display_links = ["user"]
    list_filter = ["gender", "marital_status", "employment_status", "country"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone_number",
    ]
    readonly_fields = ["user"]


    fieldsets = (
        (
            _("Personal Information"),
            {
                "fields": (
                    "user",
                    "gender",
                    "date_of_birth",
                    "marital_status",
                )
            },
        ),
        (
            _("Contact Information"),
            {"fields": ("phone_number", "address", "city", "country")},
        ),
        (
            _("Employment Information"),
            {
                "fields": (
                    "employment_status",
                    "employer_name",
                    "annual_income",
                    "date_of_employment",
                    "employer_address",
                    "employer_city",
                    "employer_state",
                )
            },
        ),
    )

    def full_name(self, obj):
        return obj.user.full_name
    
    full_name.short_description = _("Full name")

    def email(self, obj):
        return obj.user.email
    
    email.short_description = _("Email")