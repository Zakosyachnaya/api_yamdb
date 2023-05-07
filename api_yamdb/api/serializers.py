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


class UserSerializer(serializers.Serializer):
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

    # username = serializers.RegexField(
    #     required=True, max_length=150,
    #     regex=r'^[\w.@+-]',
    #     validators=[UnicodeUsernameValidator()]
    # )
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        username = value.lower()
        if username == 'me' or re.search(r'^[\w.@+-]', value) is None:
            raise ValidationError('Username не может быть "me" или @#&^@%#')
        # elif User.object.filter(username=username).exists():
        #     raise ValidationError('Username уже существует')
        # elif User.objects.filter(username=username).exists():
        #     raise ValidationError('Username уже существует')
        return value
    
    def validate(self, attrs):
        email, username = attrs.get('email'), attrs.get('username')
        if User.objects.filter(email=email, username=username).exists():
            return attrs
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username уже существует')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email уже существует')
        return attrs

        # username = data.get('username')
        # username = User.objects.filter(username=data.get('username'))
        # email = User.objects.filter(email=data.get('email'))
        # try:
        #     user, created = User.objects.get_or_create(
        #         username=username, email=email
        #     )
        # except ValidationError('ошибочка')
        # if email.exists():
        #     if username.exists():
        #         return data
        #     raise ValidationError('Email уже существует')
        # if not email.exists():
        #     if username.exists():
        #         raise ValidationError('Username уже существует')
        # return data
    

    # def validate_email(self, value):
    #     email = value.lower()
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError('Email уже существует')
# class CustomUserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         max_length=150,
#         validators=[UnicodeUsernameValidator()]
#     )
#     email = serializers.EmailField(
#         max_length=254
#     )

class SignupSerializer(UserSerializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
    
    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data.get('confirmation_code'):
            raise ValidationError('Неверный токен')
        return data