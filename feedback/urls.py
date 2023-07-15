from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import FeedbackDeleteView, FeedbackFormView, FeedbackListView

app_name = 'feedback'

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback_list'),
    path('provide_feedback', login_required(FeedbackFormView.as_view()), name='provide_feedback'),
    path('<pk>/delete/', FeedbackDeleteView.as_view(), name='delete_feedback'),
    path('<str:rating>', FeedbackListView.as_view(), name='rating'),
]
