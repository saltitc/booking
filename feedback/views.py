from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView, DeleteView
from django.views.generic.list import ListView

from .models import Feedback
from .forms import FeedbackForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from common.views import TitleMixin


class FeedbackListView(TitleMixin, ListView):
    """
    ListView with a list of reviews

    In GET: Returns a template with rating statistics and a list of reviews

    Template: feedback_list.html
    """
    template_name = 'feedback/feedback_list.html'
    model = Feedback
    context_object_name = "feeds"
    paginate_by = 3
    title = 'Отзывы'

    def get_queryset(self) -> QuerySet:
        # for filtering
        queryset = super().get_queryset()
        rating = self.kwargs.get('rating')
        if rating == 'low':
            return queryset.order_by('rating')
        if rating == 'high':
            return queryset.order_by('-rating')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['percents'] = Feedback.get_percents()
        return context


class FeedbackFormView(TitleMixin, FormView):
    """
        Feedback form template

        In GET: Returns a template with a feedback web form
        IN POST: Creates a Feedback object in the database
                 and shows a message about the successful receipt of the user's feedback

        Template: feedback.html
    """
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback:provide_feedback')
    title = 'Оставить отзыв'

    def form_valid(self, form):
        # shows a message about the successful receipt of the user's feedback
        messages.success(
            self.request,
            f'{self.request.POST["first_name"]}, спасибо за оставленный вами отзыв.')

        # creates a Feedback object
        form.save()
        return super().form_valid(form)


class FeedbackDeleteView(DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback:feedback_list')

