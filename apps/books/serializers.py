from rest_framework import serializers
from apps.books.models import (
    Category,
    Author,
    Book
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'full_name', 'bio', 'photo', 'date_of_birth']
        
class BookListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    author = serializers.CharField(source='author.full_name', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'category', 'author', 
            'price', 'stock', 'cover', 'is_in_stock'
        ]
        
class BookDetailSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'category', 'author',
            'price', 'stock', 'isbn', 'publisher', 'pages_count',
            'cover_type', 'weight_g', 'cover', 'is_in_stock', 'created_at'
        ]