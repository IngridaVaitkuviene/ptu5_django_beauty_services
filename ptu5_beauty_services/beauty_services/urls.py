from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('salons/', views.salons, name='salons'),
    path('salon/<int:pk>/', views.SalonDetailView.as_view(), name='salon'),
    path('salon/services/', views.SalonServicesView.as_view(), name='salon_services'),
    path('salon/<int:pk>/reviews/', views.SalonReviewView.as_view(), name='salon_reviews'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('my_orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('my_order/<int:pk>/', views.UserOrderDetailView.as_view(), name='user_order'),
    path('create_new_order/', views.UserOrderCreateView.as_view(), name='user_order_create'),
    path('update_order/<int:pk>/', views.UserOrderUpdateView.as_view(), name='user_order_update'),
    path('cancel_order/<int:pk>/', views.UserOrderDeleteView.as_view(), name='user_order_delete'),
]
