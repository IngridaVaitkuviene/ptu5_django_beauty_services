from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from . models import ServiceType, BeautySalon, Service, SalonService, Order, OrderLine
from . forms import SalonReviewForm, UserOrderForm, UserOrderDetailAddForm, UserOrderUpdateForm, tomorrow

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


class SalonServicesView(ListView):
    model = Service
    paginate_by = 10
    template_name = 'beauty_services/salon_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salon_id = self.request.GET.get('salon_id')
        if salon_id:
            context['object'] = get_object_or_404(BeautySalon, id=salon_id)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        salon_id = self.request.GET.get('salon_id')
        if salon_id:
            queryset = queryset.filter(salons_services__beauty_salon=salon_id)
        return queryset


class SalonReviewView(FormMixin, DetailView):
    model = BeautySalon
    form_class = SalonReviewForm
    paginate_by = 3
    template_name = 'beauty_services/salon_review.html'

    def get_success_url(self):
        return reverse('salon_reviews', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        return {
            'beauty_salon': self.get_object(),
            'customer': self.request.user.customer,
        }

    def form_valid(self, form):
        form.instance.beauty_salon = self.get_object()
        form.instance.customer = self.request.user.customer
        form.save()
        messages.success(self.request, _("Your review/comment has been posted"))
        return super().form_valid(form)


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
    paginate_by = 5

    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = queryset.filter(customer__user=self.request.user)
        return queryset


class UserOrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'beauty_services/user_order_detail.html'

    def test_func(self):
        return self.get_object().customer == self.request.user.customer


class UserOrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = UserOrderForm
    template_name = 'beauty_services/user_order_form.html'
    success_url = reverse_lazy('user_orders')

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        form.instance.status = 'n'
        messages.success(self.request, _("New order created"))
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['customer'] = self.request.user.customer
        initial['reserved_date'] = tomorrow()
        return initial


class UserOrderDetailCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = UserOrderDetailAddForm
    template_name = 'beauty_services/user_order_detail_create.html'

    def form_valid(self, form):
        messages.success(self.request, _("Details added"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_order', kwargs={'pk': self.get_object().id})

    def get_initial(self):
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['price'] = 0
        return initial

    def get_form(self, form_class=UserOrderDetailAddForm):
        form = super().get_form(form_class)
        order = self.get_object()
        if order.order_lines.count() > 0:
            salon = order.order_lines.first().salon_service.beauty_salon
            form.fields['salon_service'].queryset = SalonService.objects.filter(beauty_salon=salon)
        return form


class UserOrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = UserOrderUpdateForm
    template_name = 'beauty_services/user_order_form.html'
    success_url = reverse_lazy('user_orders')

    def test_func(self):
        return self.get_object().customer == self.request.user.customer

    def form_valid(self, form):
        form.instance.customer.user = self.request.user
        form.instance.status = 'a'
        messages.success(self.request, _("Order updated/Paid in advance"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_object()
        if context['order'].status == 'n':
            context['action'] = 'Pay advance'
        return context


class UserOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'beauty_services/user_order_delete.html'
    success_url = reverse_lazy('user_orders')

    def test_func(self):
        return self.get_object().customer == self.request.user.customer

    def form_valid(self, form):
        order = self.get_object()
        if order.status == 'a':
            messages.success(self.request, _("Order paid in advanced"))
        else:
            messages.success(self.request, _("Order deleted"))
        return super().form_valid(form)
