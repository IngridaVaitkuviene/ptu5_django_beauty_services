from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('salons/', views.salons, name='salons'),
    path('salon/<int:pk>/', views.SalonDetailView.as_view(), name='salon'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('my_orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('my_order/', views.UserOrderLineListView.as_view(), name='user_order'),
]
