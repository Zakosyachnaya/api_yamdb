from rest_framework import serializers

from reviews.models import Comment, Review
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ['author', 'text', 'score']

    def validate_review(self, review):
        user_review_exists = Review.objects.filter(
            author=self.context.get('request').user,
            title=self.context['view'].kwargs.get('title_id')).exists()
        if user_review_exists:
            raise serializers.ValidationError(
                'Отзыв пользователя на это произведение уже существует')
        return review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ['author', 'text', 'pub_date']
