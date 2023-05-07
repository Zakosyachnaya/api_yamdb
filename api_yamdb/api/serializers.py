import re
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.models import User
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=150
    )
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=254
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')


class SignupSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+\Z',
        max_length=150)
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=254
    )

    # class Meta:
    #     fields = ('email', 'username')
    #     model = User
    #     validators = (
    #         UniqueTogetherValidator(
    #             queryset=User.objects.all(),
    #             fields=['username', 'email']
    #         ),
    #     )
    
    def validate_username(self, value):
        username = value.lower()
        if username == 'me':
            raise ValidationError('Username не может быть "me" или @#&^@%#')

    def validate(self, attrs):
        email, username = attrs.get('email'), attrs.get('username')
        user = User.objects.filter(email=email, username=username)
        # # # if user.exists():
        # # #     token = RefreshToken.for_user(user) 
        # #     return (str(token.access_token), attrs)
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email уже существует')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username уже существует')
        return attrs


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=150,
        write_only=True,
    )
    confirmation_code = serializers.CharField(
        max_length=250,
        write_only=True
    )
