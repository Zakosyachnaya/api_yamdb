from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# from titles.models import Title
from users.models import User


class Review(models.Model):
    # # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='reviews'
    # )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField(max_length=3000)
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
