from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

User = get_user_model()

class ServiceType(models.Model):
    type_name = models.CharField(_("name"), max_length=50, help_text=_("Enter the name of service type"))

    class Meta:
        verbose_name = _("Service type")

    def __str__(self) -> str:
        return self.type_name

    def link_filtered_services(self):
        link = reverse('services')+'?service_type_id='+str(self.id)
        return format_html('<a href="{link}">{name}</a>', link=link, name=self.type_name)


class BeautySalon(models.Model):
    salon_name = models.CharField(_("name"), max_length=100)
    address = models.CharField(_("address"), max_length=100)
    image = models.ImageField(_("image"), upload_to='images', blank=True, null=True)
    description = HTMLField(_("description"), null=True, blank=True)

    class Meta:
        verbose_name = _("Beauty salon")
        verbose_name_plural = _("Beauty salons")
        ordering = ('salon_name',)

    def __str__(self) -> str:
        return f"{self.salon_name}, {self.address}"


class Service(models.Model):
    service_type = models.ForeignKey(
        ServiceType, 
        verbose_name=_("service type"), 
        on_delete=models.CASCADE, 
        related_name='services',
    )
    service_name = models.CharField(_("name"), max_length=100)
    price = models.DecimalField(_("price"), max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ('service_type', 'service_name',)

    def __str__(self) -> str:
        return f"{self.service_name} - {self.price}"


class SalonService(models.Model):
    beauty_salon = models.ForeignKey(
        BeautySalon, 
        verbose_name=_("beauty salon"), 
        on_delete=models.CASCADE,
        related_name='salons_services',
    )
    service = models.ForeignKey(
        Service,
        verbose_name=_("service"), 
        on_delete=models.CASCADE,
        related_name='salons_services',
    )

    class Meta:
        ordering = ('service',)

    def __str__(self) -> str:
        return f"{self.beauty_salon}: {self.service}"


class Customer(models.Model):
    phone = models.CharField(_("phone number"), max_length=50)
    user = models.OneToOneField(
        User,
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='customer',
    )

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ('user__first_name',)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}, {self.phone}, {self.user.email}"
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('n', _('new')),
        ('a', _('advance payment taken')),
        ('c', _('cancelled')),
        ('p', _('paid')),
        ('d', _('done')),
    )
    date = models.DateField(_("order date"), auto_now_add=True, editable=False)
    customer = models.ForeignKey(
        Customer, 
        verbose_name=_("customer"), 
        on_delete=models.CASCADE,
        related_name='orders',
    )
    total_sum = models.DecimalField(_("total sum"), max_digits=5, decimal_places=2, default=0)
    reserved_date = models.DateField(_("reserved date"), null=True, blank=True)
    status = models.CharField(_("status"), max_length=1, choices=STATUS_CHOICES, default='n')

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def get_total(self):
        total_sum = 0
        for line in self.order_lines.all():
            total_sum += line.total_sum
        return total_sum

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.total_sum = self.get_total()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.date} {self.total_sum} {self.customer.user.first_name} {self.customer.user.last_name}"


class OrderLine(models.Model):
    salon_service = models.ForeignKey(
        SalonService, 
        verbose_name=_("salon service"), 
        on_delete=models.CASCADE,
        related_name='order_lines',
    )
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
        related_name='order_lines',
    )
    price = models.DecimalField(_("price"), max_digits=5, decimal_places=2)
    quantity = models.IntegerField(_("quantity"), default=1)

    class Meta:
        verbose_name = _('Order line')
        verbose_name_plural = _('Order lines')

    @property
    def total_sum(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.total_sum = self.order.get_total()
        self.order.save()

    def __str__(self) -> str:
        return f"{self.salon_service}: {self.quantity} x {self.price}"


class SalonReview(models.Model):
    beauty_salon = models.ForeignKey(
        BeautySalon, 
        verbose_name=_("beauty salon"), 
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    customer = models.ForeignKey(
        Customer, 
        verbose_name=_("customer"), 
        on_delete=models.CASCADE,
        related_name='reviews',    
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=1000)

    def __str__(self) -> str:
        return f"{self.customer.user.first_name} {self.customer.user.last_name} on {self.beauty_salon} at {self.created_at}"

    class Meta:
        ordering = ('-created_at',)