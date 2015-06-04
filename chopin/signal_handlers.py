from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from ocve.models_generic import OCVEUser

@receiver(post_save, sender=User)
def user_handler(sender, instance, **kwargs):
    try:
        ocve_user = OCVEUser.objects.get(id=instance.id)
        ocve_user.username = instance.username
        ocve_user.save()
    except ObjectDoesNotExist:
        ocve_user = OCVEUser()
        ocve_user.id = instance.id
        ocve_user.username = instance.username
        ocve_user.save()
