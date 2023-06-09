# Generated by Django 3.2.18 on 2023-05-10 15:57

import django.core.validators
from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_auto_20230509_1405"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ("-pub_date",),
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AlterField(
            model_name="review",
            name="score",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="Слишком маленькое значение"
                    ),
                    django.core.validators.MaxValueValidator(
                        10, message="Слишком большое значение"
                    ),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="title",
            name="year",
            field=models.PositiveSmallIntegerField(
                blank=True,
                validators=[reviews.validators.my_year_validator],
                verbose_name="Год выпуска",
            ),
        ),
    ]
