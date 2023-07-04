from django.forms import ModelForm
from django import forms
from .models import Feedback
from studio.models import Appointment


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('first_name', 'last_name', 'email', 'service_category', 'rating', 'feedback')
        labels = {
            'first_name': "Имя",
            'last_name': "Фамилия",
            'email': "Эл. почта",
            'service_category': "Категория услуги которую вам оказывали",
            'rating': 'Оценка',
            'feedback': 'Отзыв',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите ваше имя",
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите вашу фамилию",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "example@gmail.com"
            }),
            'service_category': forms.Select(choices=Appointment.SERVICE_CHOICES, attrs={
                'class': 'form-control'
            }),
            'rating': forms.RadioSelect(choices=[
                ('1', 'rating1'),
                ('2', 'rating2'),
                ('3', 'rating3'),
                ('4', 'rating4'),
                ('5', 'rating5'),
            ],
                attrs={

                }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Ваш отзыв",
                'rows': "5",
            })}
