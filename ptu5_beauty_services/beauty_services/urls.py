from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('salons/', views.salons, name='salons'),
    path('salon/<int:pk>/', views.SalondetailView.as_view(), name='salon'),
    path('services/', views.ServiceListView.as_view(), name='services'),
]
