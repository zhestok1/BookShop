from rest_framework import serializers
from apps.payments.models import Order, OrderItem, Payment
from apps.books.serializers import BookListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'price', 'quantity']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'transaction_id', 'amount', 'status', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'items', 'payment', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'total_amount', 'created_at']