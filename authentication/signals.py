from django.db.models.signals import post_save
from .models import User, UserProfile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ receiver function that will create profile for an user instance

    Args:
        sender ([model class]): [user model class]
        instance ([model object]): [user model instance that is actually being saved]
        created ([boolean]): [true if new record has created in user model]
    """
    if created:
        UserProfile.objects.create(user=instance)

