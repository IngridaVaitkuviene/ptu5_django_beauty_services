from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import ServiceType, BeautySalon, Service


def index(request):
    types =  ServiceType.objects.all()
    salon_count = BeautySalon.objects.count()
    service_count = Service.objects.count()
    context = {
        'service_type': " | ".join(str(t) for t in types),
        'salon_count': salon_count,
        'service_count': service_count,
    }
    return render(request, 'beauty_services/index.html', context)

def salons(request):
    paginator = Paginator(BeautySalon.objects.all(), 15)
    page_number = request.GET.get('page')
    paged_salons = paginator.get_page(page_number)
    return render(request, 'beauty_services/salons.html', {'salons': paged_salons})


class SalonDetailView(DetailView):
    model = BeautySalon
    template_name = 'beauty_services/salon_detail.html'

# def salon(request, salon_id):
#     context = {
#         'salon': get_object_or_404(BeautySalon, id=salon_id),
#     }
#     return render(request, 'beauty_services/salon.html', context)

class ServiceListView(ListView):
    model = Service
    paginate_by = 15
    template_name = 'beauty_services/services_list.html'
