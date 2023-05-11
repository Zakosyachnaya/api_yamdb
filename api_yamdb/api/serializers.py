import re

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True,
        regex=r"^[\w.@+-]",
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "bio", "role")

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError('Username не может быть "me"')
        if not re.match(r"[\w.@+-]+\Z", value):
            raise ValidationError("Username не может быть @#&^@%#")
        return value


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError('Username не может быть "me"')
        if not re.match(r"[\w.@+-]+\Z", value):
            raise ValidationError("Username не может быть @#&^@%#")
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")
        model = User


class SimpleUser(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True, regex=r"^[\w.@+-]+\Z", max_length=150
    )

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "bio", "role")
        read_only_fields = ("role",)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Review
        fields = ("author", "text", "score", "id", "pub_date")

    def validate(self, review):
        if self.context["request"].method != "POST":
            return review
        else:
            user_review_exists = Review.objects.filter(
                author=self.context.get("request").user,
                title=self.context["view"].kwargs.get("title_id"),
            ).exists()
            if user_review_exists:
                raise serializers.ValidationError(
                    "Отзыв пользователя на это произведение уже существует"
                )
            else:
                return review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("author", "text", "pub_date", "id")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = "__all__"
