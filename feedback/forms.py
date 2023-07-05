from django.forms import ModelForm
from django import forms
from .models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('user', 'first_name', 'last_name', 'email', 'rating', 'feedback')
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
        error_messages = {
            'user': {
                'unique': "Вы уже оставили отзыв",
            },
        }
