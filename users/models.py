from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]

    phone = models.CharField(
        max_length=15, null=True, verbose_name='Телефон', validators=[RegexValidator(
            regex=r'\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b',
            message='Неверный формат номера телефона.'
        )])
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    gender = models.CharField(max_length=2, verbose_name='Пол', choices=GENDER_CHOICES, default=MALE)
