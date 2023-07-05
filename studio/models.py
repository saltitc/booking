from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator
from django.template.loader import get_template
from django.core.mail import EmailMessage
import datetime
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now
from users.models import User

class Appointment(models.Model):
    """
    Database table model for appointments

    fields: first_name, last_name, email, phone,
                message, sent_date, accepted, accepted_date
    """
    DEFAULT = 'DF'
    RECORDING = 'RC'
    MASTERING = 'MS'
    MIXING = 'MX'
    GHOSTWRITING = 'GW'

    SERVICE_CHOICES = [
        (DEFAULT, 'Выберите категорию услуги'),
        (RECORDING, 'Звукозапись'),
        (MASTERING, 'Мастеринг'),
        (MIXING, 'Сведение'),
        (GHOSTWRITING, 'Написание текста'),
    ]

    user = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(
        max_length=15, verbose_name='Имя', validators=[MinLengthValidator(
            limit_value=2, message='Убедитесь, что поле имени содержит не менее 2 символов.'
        )])
    last_name = models.CharField(
        max_length=20, verbose_name='Фамилия', validators=[MinLengthValidator(
            limit_value=2, message='Убедитесь, что поле фамилии содержит не менее 2 символов.'
        )])
    email = models.EmailField(
        max_length=25, verbose_name='Эл. почта', validators=[EmailValidator(
            message='Введите корректный адрес электронной почты.'
        )])
    phone = models.CharField(
        max_length=15, null=True, verbose_name='Телефон', validators=[RegexValidator(
            regex=r'\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b',
            message='Неверный формат номера телефона.'
        )])
    date = models.DateField(null=True, verbose_name='Дата записи', )
    service_category = models.CharField(max_length=2, verbose_name='Категория', choices=SERVICE_CHOICES,
                                        default=DEFAULT)
    message = models.TextField(
        verbose_name='Сообщение к заявке', validators=[MinLengthValidator(
            limit_value=15, message='Убедитесь, что поле с сообщением содержит не менее 15 символов.'
        )])
    time = models.TimeField(null=True, blank=True, verbose_name='Время записи')
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения заявки')
    accepted = models.BooleanField(default=False, verbose_name='Принята', )
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name='Дата принятия заявки')
    is_confirmed = models.BooleanField(default=False, verbose_name='Потверждена')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def accept_appointment(cls, id, date, time):
        """
        Method for changing is_accepted status of an appointment
        """
        appointment = Appointment.objects.get(id=id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.date = datetime.datetime.strptime(date, '%Y-%m-%d')
        appointment.time = datetime.datetime.strptime(time, '%H:%M')
        appointment.save()
        return appointment

    class Meta:
        ordering = ['-date']


class AppointmentConfirmation(models.Model):
    """
    Database table model for appointment confirmation

    fields: code, appointment, created, expiration
    """
    code = models.UUIDField(unique=True)
    appointment = models.ForeignKey(to=Appointment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Подтверждение записи ({self.appointment})'

    def send_confirmation_email(self):
        """
        Sends an email with a confirmation link
        """
        # generates a confirmation link
        link = reverse('studio:appointment_confirmation', kwargs={
            'email': self.appointment.email,
            'code': self.code
        })
        # render data
        data = {
            'first_name': self.appointment.first_name,
            'dt': self.appointment.date,
            'tm': self.appointment.time,
            'service': self.appointment.get_service_category_display,
            'link_for_confirmation': f"{settings.DOMAIN_NAME}{link}"
        }
        # renders html template to send to email
        message = get_template('studio/email_response.html').render(data)

        # create and send email
        email = EmailMessage(
            subject=f'Подтверждение записи',
            body=message,
            from_email=f'Студия <{settings.EMAIL_HOST_USER}>',
            to=[self.appointment.email]
        )
        email.content_subtype = 'html'
        email.send()

    def is_expired(self) -> bool:
        return now() >= self.expiration
