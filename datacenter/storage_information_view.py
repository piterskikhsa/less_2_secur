from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):

    non_closed_visits = Visit.objects.filter(leaved_at=None)
 
    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
