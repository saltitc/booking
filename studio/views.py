from common.views import TitleMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import AppointmentForm
from django.contrib import messages


class HomeTemplateView(TitleMixin, TemplateView):
    """
    Template view, which displays the home page.
    For administration and staff, the number of new applications,
    the admin panel and application management are additionally shown
    """
    template_name = 'studio/index.html'
    title = 'Главная страница'


class AppointmentFormView(TitleMixin, FormView):
    """
    FormView for booking an appointment from the user to the administration of the studio,
    to receive the service on the date selected by the user and approved by the studio

    In GET: Returns a template with a web form that can be filled out to receive a service
    IN POST: Creates an Appointment object in the database
             and shows a message about the successful receipt of the user's application

    Template: appointment.html
    """
    form_class = AppointmentForm
    template_name = 'studio/appointment.html'
    success_url = reverse_lazy('studio:appointment')
    title = 'Оформление заявки на получение услуг'

    def form_valid(self, form):
        # shows a message about the successful receipt of the user's application
        messages.success(
            self.request,
            f'{self.request.POST["first_name"]}, заявка отправлена. Ответ придет на указанную электронную почту')

        # creates an Appointment object
        form.save()
        return super().form_valid(form)
