from django.contrib import admin
from .models import Appointment, AppointmentConfirmation


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'email', 'service_category',
        'accepted', 'is_confirmed', 'date', 'time'
    )
    fieldsets = (
        ('Персональная информация', {
            'fields': (('first_name', 'last_name'), ('email', 'phone'))
        }),
        ('Техническая информация', {
            'fields': (
            'service_category', 'message', ('date', 'time'), 'is_confirmed', 'accepted', 'accepted_date', 'sent_date')
        }),
    )
    readonly_fields = ('sent_date', 'accepted_date', 'accepted', 'is_confirmed')
    search_fields = ('email', 'phone')
    ordering = ('-date',)
    list_per_page = 15
    list_filter = ('accepted', 'date', 'service_category')
    empty_value_display = "Не указано"


@admin.register(AppointmentConfirmation)
class AppointmentConfirmationAdmin(admin.ModelAdmin):
    list_display = ('code', 'appointment', 'created', 'expiration')
    fields = ('code', 'appointment', 'created', 'expiration')
    readonly_fields = ('created', 'appointment')
    search_fields = ('appointment',)
    ordering = ('created',)
    empty_value_display = "Не указано"
