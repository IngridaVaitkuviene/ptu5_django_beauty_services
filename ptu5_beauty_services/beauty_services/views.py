from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import ServiceType, BeautySalon, Service, Order, OrderLine

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
    salons = BeautySalon.objects.all()
    search = request.GET.get('search')
    if search:
        salons = salons.filter(salon_name__icontains=search)
    paginator = Paginator(salons, 3)
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

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(service_name__icontains=search)| Q(service_type__type_name__icontains=search))
        service_type_id = self.request.GET.get('service_type_id')
        if service_type_id:
            queryset = queryset.filter(service_type__id=service_type_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_type_id = self.request.GET.get('service_type_id')
        context['service_types'] = ServiceType.objects.all
        if service_type_id:
            context['service_type'] = get_object_or_404(ServiceType, id=service_type_id)
        return context


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'beauty_services/user_order_list.html'
    # paginate_by = 10

    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = queryset.filter(customer__user=self.request.user)
        return queryset

class UserOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'beauty_services/user_order_detail.html'
    # paginate_by = 10
