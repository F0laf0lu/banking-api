from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.userauth"
    verbose_name = _("User Auth")
