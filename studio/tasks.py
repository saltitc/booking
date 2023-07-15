import uuid

from celery import shared_task

from studio.models import Appointment, AppointmentConfirmation


@shared_task
def send_email_confirmation(appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    # creates an AppointmentConfirmation object
    confirmation = AppointmentConfirmation.objects.create(
        code=uuid.uuid4(),  # generates a unique code for the verification link
        appointment=appointment,  # appointment object for which the link will be created
        expiration=appointment.date  # link expiration date
    )

    # sends a message to the user's mail with a link to confirm an appointment
    confirmation.send_confirmation_email()
