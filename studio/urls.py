from django.urls import path
from django.contrib.auth.decorators import login_required

from studio.views import (HomeTemplateView, AppointmentFormView, ManageAppointmentsListView,
                          AppointmentConfirmationView, AppointmentDeleteView)

app_name = 'studio'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='index'),
    path('make_an_appointment/', login_required(AppointmentFormView.as_view()), name='appointment'),
    path('manage_appointments/', ManageAppointmentsListView.as_view(), name='manage'),
    path('confirm/<str:email>/<uuid:code>/', AppointmentConfirmationView.as_view(), name='appointment_confirmation'),
    path('<pk>/delete/', AppointmentDeleteView.as_view(), name='delete_appointment'),

    path(
        'manage_appointments/category/<str:category_abbreviation>/',
        ManageAppointmentsListView.as_view(),
        name='service_category'
    ),
    path(
        'manage_appointments/accepted/<int:is_accepted>/',
        ManageAppointmentsListView.as_view(),
        name='is_accepted'
    ),
    path(
        'manage_appointments/relevance/<int:is_relevant>/',
        ManageAppointmentsListView.as_view(),
        name='is_relevant'
    ),
]
