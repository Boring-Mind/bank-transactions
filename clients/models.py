from django.contrib.auth.models import AbstractUser, UserManager
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class ClientManager(UserManager):
    def create(self, *args, **kwargs):
        """Override default create method.

        Create_user method is needed
        for proper password hashing
        and field validation.
        """
        return super().create_user(*args, **kwargs)


class Client(AbstractUser):
    patronymic = models.CharField(max_length=190, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    passport_number = models.CharField(max_length=10, unique=True)

    objects = ClientManager()


@receiver(post_delete, sender=Client)
def remove_user_from_cache(sender, instance, **kwargs):
    """Invalidate jwt user cache."""
    cache.delete(f'jwt_user_{instance.id}')
