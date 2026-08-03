from django.urls import path
from apps.payments.views import CheckoutView, OrderListView, OrderDetailView

urlpatterns = [
    # Оформление заказа
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    # История заказов пользователя
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]