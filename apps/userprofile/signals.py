from django.db.models.signals import post_save
from django.dispatch import receiver
from loguru import logger

from core.settings.base import AUTH_USER_MODEL
from apps.userprofile.models import Profile


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for {instance.first_name} {instance.last_name}")