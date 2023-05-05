import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    #     max_length=50,
    #     min_length=6,
    #     write_only=True
    # )
    # username = serializers.CharField(
    #     required=True, max_length=150
    # )
    # email = serializers.EmailField(
    #     required=True,  max_length=254
    # )
    # email = serializers.EmailField(
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    #     )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    role = serializers.ReadOnlyField()
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, value):
        username = value.lower()
        if username == 'me' or re.search(r'^[\w.@+-]', value) is None:
            raise ValidationError('Username не может быть "me" или @#&^@%#')
        return value
    
class MeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254
    )
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email уже существует')
# class CustomUserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         max_length=150,
#         validators=[UnicodeUsernameValidator()]
#     )
#     email = serializers.EmailField(
#         max_length=254
#     )


#     class Meta:
#         model = User
#         fields = '__all__'

#     def validate_email(self, value):
#         email = value.lower()
#         if User.objects.filter(email=email).exists():
#             raise ValidationError('Email уже существует')
    #  def validate_username(self, value):
    #     username = value.lower()
    #     # email = value.lower()
    #     if username == 'me' or re.search(r'^[\w.@+-]', value) is None:
    #         raise ValidationError('Username не может быть "me" или @#&^@%#')
    #     # elif User.object.filter(username=username).exists():
    #     #     raise ValidationError('Username уже существует')
    #     return value

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    # username = serializers.RegexField(
    #     required=True, max_length=150,
    #     regex=r'^[\w.@+-]',
    #     validators=[UnicodeUsernameValidator()]
    # )
    email = serializers.EmailField(
        required=True, max_length=254
    )
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        username = value.lower()
        # email = value.lower()
        if username == 'me' or re.search(r'^[\w.@+-]', value) is None:
            raise ValidationError('Username не может быть "me" или @#&^@%#')
        # elif User.object.filter(username=username).exists():
        #     raise ValidationError('Username уже существует')
        return value

    def validate(self, data):
        username = User.objects.filter(username=data['username'])
        email = User.objects.filter(email=data['email'])
        if email.exists():
            if username.exists():
                return data
            raise ValidationError('Email уже существует')
        if not email.exists():
            if username.exists():
                raise ValidationError('Username уже существует')
        return data


class TokenSerializer(TokenObtainPairSerializer):
    # username = serializers.CharField(
    #     required=True, max_length=150
    # )
    username = serializers.CharField(
        required=True, max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
    
    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.exists():
            raise ValidationError('Username уже существует')
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный токен')
        return data