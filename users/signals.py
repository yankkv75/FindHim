from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


# @receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user, username=user.username,
                                         email=user.email, name=user.first_name)


def update_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created is False:  # Без if запустится функция create_profile и запустится бесконечный цикл
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(create_profile, sender=User)
post_save.connect(update_profile, sender=Profile)
post_delete.connect(delete_profile, sender=Profile)
