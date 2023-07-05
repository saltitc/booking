from django.db.models import QuerySet
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import Appointment, AppointmentConfirmation
from django.views.generic import ListView
from django.views.generic.edit import FormView
from common.views import TitleMixin
from .forms import AppointmentForm
import datetime
from django.shortcuts import HttpResponseRedirect
import uuid


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
            f'{self.request.POST["first_name"]}, заявка отправлена. Ответ придет на вашу электронную почту')

        # creates an Appointment object
        form.save()
        return super().form_valid(form)


class ManageAppointmentsListView(TitleMixin, ListView):
    """
    ListView with a list of applications for services in which it can be accepted

    In GET: Returns a template with a list of applications
    IN POST: Application is accepted with the date and time of the meeting

    Template: manage-appointments.html
    """
    title = 'Управление заявками'
    template_name = 'studio/manage-appointments.html'
    model = Appointment
    context_object_name = 'appointments'
    login_required = True
    paginate_by = 3
    ordering = 'date'

    def post(self, request) -> HttpResponseRedirect:

        # changing the accepted status of the appointment
        appointment = self.model.accept_appointment(
            id=request.POST.get('appointment-id'),
            date=request.POST.get('date'),
            time=request.POST.get('time')
        )

        # creates an AppointmentConfirmation object
        confirmation = AppointmentConfirmation.objects.create(
            code=uuid.uuid4(),  # generates a unique code for the verification link
            appointment=appointment,  # appointment object for which the link will be created
            expiration=appointment.date  # link expiration date
        )

        # sends a message to the user's mail with a link to confirm an appointment
        confirmation.send_confirmation_email()

        # shows a message that the user has been enrolled successfully
        messages.add_message(request, messages.SUCCESS, f"{appointment} записан")

        return HttpResponseRedirect(request.path)

    def get_queryset(self) -> QuerySet:
        # for filtering
        queryset = super().get_queryset()
        category_abbreviation = self.kwargs.get('category_abbreviation')
        is_accepted = self.kwargs.get('is_accepted')
        is_relevant = self.kwargs.get('is_relevant')
        if is_accepted is not None:
            return queryset.filter(accepted=is_accepted)
        if category_abbreviation:
            return queryset.filter(service_category=category_abbreviation)
        if is_relevant is not None:
            return queryset.filter(date__gte=datetime.date.today()) if is_relevant \
                else queryset.filter(date__lt=datetime.date.today())
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManageAppointmentsListView, self).get_context_data()
        context['categories'] = Appointment.SERVICE_CHOICES[1:]
        return context


class AppointmentConfirmationView(TitleMixin, TemplateView):
    """
    TemplateView to confirm appointment

    In GET: Returns a template about the successful confirmation of appointment

    Template: appointment_confirmation.html
    """
    title = 'Подтверждение заявки'
    template_name = 'studio/appointment_confirmation.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']  # takes uuid code from request
        # looking for AppointmentConfirmation object by code
        appointment_confirmation = AppointmentConfirmation.objects.filter(code=code)

        # checking if an object exists and has not expired
        if appointment_confirmation.exists() and not appointment_confirmation.first().is_expired():
            appointment = appointment_confirmation.first().appointment
            appointment.is_confirmed = True
            appointment.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
