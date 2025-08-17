from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile, CustomUser

from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
        )

        subject = 'Welcome to Market Edge'
        message = f'This email serves as confirmation being sent to {user.username}, registered to the following email {user.email}.'

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
            )
        except:
            print('Email failed to send properly.')


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.username = profile.username
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=CustomUser)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
