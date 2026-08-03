from django.contrib import admin
from apps.payments.models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'price', 'quantity']
    can_delete = False
    
class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['transaction_id', 'amount', 'status', 'created_at']
    can_delete = False
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__username', 'user__email']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    
    # Встраиваем позиции заказа и платеж прямо на страницу заказа
    inlines = [OrderItemInline, PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'status', 'transaction_id', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['transaction_id', 'order__id', 'order__user__username']
    readonly_fields = ['created_at']

