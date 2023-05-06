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
    # slug = models.SlugField(unique=True)
    # id = models.AutoField(primary_key=True)
    # is_active = models.BooleanField(default=True)
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
    # first_name = models.CharField(db_index=True, max_length=150)
    # last_name = models.CharField(db_index=True, max_length=150)
    username = models.CharField(
        max_length=150,
        null=False, blank=False,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        null=False, blank=False
    )

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return{
    #         'refresh':str(refresh),
    #         'access':str(refresh.access_token)
    #     }

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
    
    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    # @property
    # def is_user(self):
    #     return self.role == self.USER

    # def __str__(self):
    #     return self.username

    # class Meta:
    #     ordering = ('id',)
    #     constraints = [
    #         models.CheckConstraint(
    #             check=~models.Q(username__iexact='me'),
    #             name='unique_name_owner'
    #         )
    #     ]  
