from django_filters.rest_framework import DjangoFilterBackend   
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import filters
from .models import Category, Author, Book
from .serializers import (
    CategorySerializer,
    AuthorSerializer,
    BookListSerializer,
    BookDetailSerializer
)

from .filters import BookFilter

class BookListView(ListAPIView):
    queryset = Book.objects.filter(is_active=True).select_related('category', 'author')
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    
    filterset_class = BookFilter
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
     
    # Работа поисковой строки
    search_fields = ['title', 'author__first_name', 'author__last_name', 'isbn']
    
    # Сортировка по цене и дате
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']
    
    
class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.filter(is_active=True).select_related('category', 'author')
    serializer_class = BookDetailSerializer
    permission_classes = [AllowAny]
    
class CategoryDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
class AuthorDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    
    
