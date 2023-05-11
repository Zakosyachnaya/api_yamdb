from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import my_year_validator


class Category(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Название категории"
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название жанра")
    slug = models.SlugField(unique=True, verbose_name="Слаг жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Название произведения"
    )
    year = models.PositiveSmallIntegerField(
        blank=True, validators=[my_year_validator],
        verbose_name="Год выпуска"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="titles",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField(max_length=3000)
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Слишком маленькое значение"),
            MaxValueValidator(10, message="Слишком большое значение"),
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (
            models.UniqueConstraint(
                fields=("author", "title"),
                name="unique_author_review",
            ),
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
