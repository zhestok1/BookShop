from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    raw_id_fields = ['book']  
    readonly_fields = ['get_total_price']

    @admin.display(description='Итого за товар')
    def get_total_price(self, obj):
        return obj.total_price


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_total_price', 'created_at', 'updated_at']
    search_fields = ['user__email', 'user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price']
    inlines = [CartItemInline]

    def get_queryset(self, request):
        # Оптимизируем запросы: подтягиваем юзера, товары и книги за 1 запрос!
        return super().get_queryset(request).select_related('user').prefetch_related('items__book')

    @admin.display(description='Общая сумма')
    def get_total_price(self, obj):
        return f"{obj.total_price} руб."


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'get_book_title', 'quantity', 'get_total_price']
    search_fields = ['book__title', 'cart__user__email']
    raw_id_fields = ['cart', 'book']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cart__user', 'book')

    @admin.display(description='Книга', ordering='book__title')
    def get_book_title(self, obj):
        return obj.book.title

    @admin.display(description='Итого')
    def get_total_price(self, obj):
        return f"{obj.total_price} руб."