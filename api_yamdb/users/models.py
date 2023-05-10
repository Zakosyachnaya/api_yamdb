from django.contrib.auth.models import AbstractUser
from django.db import models


class RolesModels:
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    choices = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор')
    )


class User(AbstractUser):

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=RolesModels.choices,
        default=RolesModels.USER
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == RolesModels.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == RolesModels.ADMIN
