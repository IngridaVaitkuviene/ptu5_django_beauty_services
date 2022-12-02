from django.shortcuts import render
from . models import ServiceType, BeautySalon

def index(request):
    types =  ServiceType.objects.all()
    context = {'service_type': " | ".join(str(t) for t in types)}
    return render(request, 'beauty_services/index.html', context)
