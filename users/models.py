from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('moderator', 'Moderator'),
    )
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default='client')
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",  # измененное related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # измененное related_name
        related_query_name="user",
    )

    def __str__(self):
        return self.username
