from rest_framework import serializers

from ..users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=50,
        min_length=6,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)