from .models import Appointment


def get_notification(request):
    count = Appointment.objects.filter(accepted=False).count()
    data = {
        'count_of_not_accepted_appointments': count
    }
    return data