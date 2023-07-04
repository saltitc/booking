from django.forms import ModelForm
from django import forms
from .models import Appointment


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(ModelForm):
    """
    Form that can be filled out to receive a service

    Model: booking.Appointment
    """

    class Meta:
        model = Appointment
        fields = ('first_name', 'last_name', 'email', 'phone', 'message', 'date', 'service_category')
        labels = {
            'first_name': "Имя",
            'last_name': "Фамилия",
            'email': "Эл. почта",
            'phone': "Номер телефона",
            'message': 'Cообщение',
            'date': 'Дата',
            'service_category': 'Категория услуг'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control-label px-3',
                'placeholder': "Введите ваше имя"}),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control-label px-3',
                'placeholder': "Введите вашу фамилию"}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control-label px-3',
                'placeholder': "example@gmail.com"}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control-label px-3',
                'placeholder': "8-999-999-99-99"}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Ваши пожелания по оказанию услуги",
                'rows': "5"}),
            'date': DateInput(),
            'service_category': forms.Select(choices=Appointment.SERVICE_CHOICES, attrs={
                'class': 'form-control',
                'style': 'padding: 8px 15px; margin: 5px 0px; height: 49px;'
            })
        }
