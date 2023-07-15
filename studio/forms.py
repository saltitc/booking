from django import forms
from django.forms import ModelForm

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
        fields = ('user', 'first_name', 'last_name', 'email', 'phone', 'message', 'date', 'service_category')
        labels = {
            'message': 'Cообщение',
            'date': 'Дата',
            'service_category': 'Категория услуг'
        }
        widgets = {
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
