from datetime import datetime

from django.core.exceptions import ValidationError


def my_year_validator(value):
    if value > datetime.now().year:
        raise ValidationError("Год выпуска не может быть больше текущего года.")
