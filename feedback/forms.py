from django.forms import ModelForm
from django import forms
from .models import Feedback
from studio.models import Appointment


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('rating', 'feedback')
        labels = {
            'rating': 'Оценка',
            'feedback': 'Отзыв',
        }
        widgets = {
            'rating': forms.RadioSelect(choices=[
                ('1', 'rating1'),
                ('2', 'rating2'),
                ('3', 'rating3'),
                ('4', 'rating4'),
                ('5', 'rating5'),
            ]),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Ваш отзыв",
                'rows': "5",
            })}
