from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.timezone import now


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
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"Подтверждение почты для пользователя {self.user.email}"

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration
