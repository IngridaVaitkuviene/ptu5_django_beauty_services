from django.contrib import admin
from . import models

class BeautySalonAdmin(admin.ModelAdmin):
    list_display = ('salon_name', 'address',)
    search_fields = ('salon_name', 'address',)

admin.site.register(models.ServiceType)
admin.site.register(models.BeautySalon, BeautySalonAdmin)
admin.site.register(models.Service)
admin.site.register(models.SalonService)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderLine)