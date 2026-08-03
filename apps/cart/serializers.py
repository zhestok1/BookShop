from rest_framework import serializers
from apps.books.serializers import BookListSerializer
from apps.cart.models import Cart, CartItem
from apps.users.models import User
from apps.books.models import Book

class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
        
class CartItemSerializer(serializers.ModelSerializer):
    
    book = BookListSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'total_price']
        
class CartSerializer(serializers.ModelSerializer):
    
    user = CartUserSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'updated_at']
        
class AddToCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

    def validate_book_id(self, value):
        if not Book.objects.filter(id=value).exists():
            raise serializers.ValidationError('Книги с таким ID не существует!')
        return value