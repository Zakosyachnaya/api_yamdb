from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# from rest_framework_simplejwt.tokens import AccessToken


class User(AbstractUser, PermissionsMixin):
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
    first_name = models.CharField(db_index=True, max_length=150)
    last_name = models.CharField(db_index=True, max_length=150)
    username = models.CharField(
        db_index=True, max_length=150,
        blank=False, null = False
    )
    email = models.EmailField(
        db_index=True,  max_length=254,
        blank=False, null = False
    )

    @property
    def moder(self):
        return self.role == self.MODERATOR
    
    @property
    def admn(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]
    
    def __str__(self):
        return self.email

    # class Meta:
    #     ordering = ('id',)
    #     constraints = [
    #         models.CheckConstraint(
    #             check=~models.Q(username__iexact='me'),
    #             name='unique_name_owner'
    #         )
    #     ]  

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

    # def generate_jwt_token(self):
    #     dt = datetime.now() + timedelta(days=1)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode('utf-8')
