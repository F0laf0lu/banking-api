from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class UserprofileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.userprofile"
    verbose_name = _("User Profile")

    def ready(self) -> None:
        import apps.userprofile.signals