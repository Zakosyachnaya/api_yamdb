from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
# from rest_framework_simplejwt.tokens import AccessToken


class User(AbstractUser, PermissionsMixin):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    username = models.CharField(db_index=True, max_length=35, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    # def generate_jwt_token(self):
    #     dt = datetime.now() + timedelta(days=1)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode('utf-8')
