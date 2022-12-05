from django.contrib import admin
from . import models

class BeautySalonAdmin(admin.ModelAdmin):
    list_display = ('salon_name', 'address', 'get_service_types',)
    search_fields = ('salon_name', 'address',)

    @admin.display(description='service type')
    def get_service_types(self, obj):
        salonservices = obj.salons_services.all().values('service')
        types = models.ServiceType.objects.filter(services__in=salonservices).distinct()
        return ", ".join(str(t) for t in types)


class SalonServiceAdmin(admin.ModelAdmin):
    list_display = ('beauty_salon', 'service',)
    search_fields = ('beauty_salon', 'service',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'price', 'service_type')
    list_filter = ('service_type',)
    search_fields = ('service_name', 'price',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'phone',)
    search_fields = ('user', 'phone',)

    @admin.display(description='full name', ordering='user__last_name')
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    @admin.display(description='email')
    def get_email(self, obj):
        return f"{obj.user.email}"


class OrderLineInLine(admin.TabularInline):
    model = models.OrderLine
    extra = 0
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'total_sum', 'reserved_date', 'status',)
    list_filter = ('date', 'status',)
    list_editable = ('status', 'reserved_date')
    readonly_fields = ('date',)
    search_fields = (
        'date', 
        'customer__phone', 'customer__user__first_name', 'customer__user__last_name',
        'total_sum', 
        'reserved_date', 
        'status',
    ) 
    inlines = (OrderLineInLine, )
    
    fieldsets = (
        ('General', {'fields': ('date', 'customer',)}),
        ('Reservation', {'fields': ('reserved_date','status', 'total_sum', )}),
    )


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('salon_service', 'quantity', 'price', 'total_sum', 'order',)
    search_fields = (
        'order__date',
        'order__customer__user__first_name',
        'order__customer__user__last_name',
        'salon_service__beauty_salon__salon_name', 
        'salon_service__service__service_name',
    )

    
admin.site.register(models.ServiceType)
admin.site.register(models.BeautySalon, BeautySalonAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.SalonService, SalonServiceAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)