from django.urls import path

from studio.views import HomeTemplateView

app_name = 'studio'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='index'),
]
