from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=role_choices,
        default=USER,
    )
    # first_name = models.CharField(db_index=True, max_length=150)
    # last_name = models.CharField(db_index=True, max_length=150)
    # username = models.CharField(
    #     db_index=True, max_length=150,
    #     blank=False, null = False,
    #     unique=True
    # # )
    # email = models.EmailField(
    #     db_index=True,  max_length=254,
    #     blank=False, null = False
    # )

    @property
    def moderator(self):
        return self.role == self.MODERATOR
    
    @property
    def admin(self):
        return self.role == self.ADMIN

    @property
    def user(self):
        return self.role == self.USER

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username 

    # class Meta:
    #     ordering = ('id',)
    #     constraints = [
    #         models.CheckConstraint(
    #             check=~models.Q(username__iexact='me'),
    #             name='unique_name_owner'
    #         )
    #     ]  
