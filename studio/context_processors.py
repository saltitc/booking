from .models import Appointment


def get_notification(request):
    count = Appointment.objects.filter(accepted=False).count()
    data = {
        'count_of_not_accepted_appointments': count
    }
    return data


def get_user_appointments(request):
    user = request.user
    return {'user_appointments': Appointment.objects.filter(user=user.id) if user.is_authenticated else []}
