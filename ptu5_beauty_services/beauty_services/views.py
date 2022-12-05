from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import ServiceType, BeautySalon, Service, OrderLine

def index(request):
    types =  ServiceType.objects.all()
    salon_count = BeautySalon.objects.count()
    service_count = Service.objects.count()
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1

    context = {
        'service_type': " | ".join(str(t) for t in types),
        'salon_count': salon_count,
        'service_count': service_count,
        'visits_count': visits_count,
    }
    return render(request, 'beauty_services/index.html', context)

def salons(request):
    paginator = Paginator(BeautySalon.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_salons = paginator.get_page(page_number)
    return render(request, 'beauty_services/salons.html', {'salons': paged_salons})


class SalonDetailView(DetailView):
    model = BeautySalon
    template_name = 'beauty_services/salon_detail.html'


class ServiceListView(ListView):
    model = Service
    paginate_by = 15
    template_name = 'beauty_services/services_list.html'


class UserOrderListView(LoginRequiredMixin, ListView):
    model = OrderLine
    template_name = 'beauty_services/user_order_list.html'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset =  super().get_queryset()
    #     queryset = queryset.filter(customer=self.request.user)
    #     return queryset

