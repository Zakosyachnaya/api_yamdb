from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework_simplejwt.tokens import AccessToken


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    role_choices = (
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=role_choices,
        blank=True,
        default='user',
    )
    username = models.CharField(
        max_length=150,
        null=False, blank=False,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        null=False, blank=False
    )
    class Meta:
        ordering = ('role',)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
    
    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN