import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_saved_handler(sender, instance, created, **kwargs):
    if created:
        logger.info("User %s saved, creating a profile", instance)
        Profile.objects.create(user=instance)
