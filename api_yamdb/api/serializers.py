from django.contrib.auth import authenticate
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=50,
        min_length=6,
        write_only=True
    )
    # username = serializers.CharField(
    #     required=True, max_length=150
    # )
    # email = serializers.EmailField(
    #     required=True,  max_length=254
    # )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def username_email_validation(self, value):
        if value == 'me':
            raise serializers.ValidationError('Такой username запрещен')
    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)
    

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True, max_length=150,
        regex=r'^[\w.@+-]'
    )
    email = serializers.EmailField(
        required=True, max_length=254
    )
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        User.objects.create(user=user)
        return user
    def clean(self):
        username = self.validated_data.get('username')
        if username.lower() == 'me':
            raise ValidationError('Username cannot be "me"')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        password = attrs.get('password')
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get('request'), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail('attempt_failed')
        if self.user:
            return attrs
        self.fail('attempt_failed')