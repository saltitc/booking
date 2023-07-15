from itertools import tee

from django.core.validators import EmailValidator, MinLengthValidator
from django.db import models

from users.models import User


class Feedback(models.Model):
    # class Meta:
    #     ordering = ['-date']

    user = models.OneToOneField(to=User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь')
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
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    feedback = models.TextField(
        verbose_name='Отзыв', validators=[MinLengthValidator(
            limit_value=5, message='Убедитесь, что поле с отзывом содержит не менее 5 символов.'
        )])
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_percents(cls) -> dict[str, int | list[dict]]:
        """
        Returns the average rating of the reviews and
        the percentage of the total number of reviews for each rating
        """
        # count of reviews
        feedback_count = Feedback.objects.all().count()

        if feedback_count == 0:
            return {
                'average': 0,
                'percents': [{'stars': rating, 'percent': 0} for rating in range(5, 0, -1)]
            }

        one_percent = feedback_count / 100

        # 2 iterators that contain the number of reviews for each rating
        rating_counts_1, rating_counts_2 = tee(
            (Feedback.objects.filter(rating=rating).count() for rating in range(1, 6)),
            2
        )
        # the sum of the number of reviews of each rating
        rating_sum = sum(count * rating for rating, count in enumerate(rating_counts_1, 1))

        return {
            'average': round(rating_sum / feedback_count, 1),
            # percentage for each rating of the total number of reviews
            'percents': reversed([{'stars': rating, 'percent': round(count // one_percent)}
                                  for rating, count in enumerate(rating_counts_2, 1)]),
        }
