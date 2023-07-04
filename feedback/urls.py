from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import FeedbackFormView, FeedbackListView

app_name = 'feedback'

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback_list'),
    path('provide_feedback', login_required(FeedbackFormView.as_view()), name='provide_feedback'),
    path('<str:rating>', FeedbackListView.as_view(), name='rating'),
]
