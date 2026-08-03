from django.urls import path
from apps.books.views import (
    BookListView,
    BookDetailView,  # Исправлена опечатка (BookDetaiLView -> BookDetailView)
    AuthorDetailView,
    CategoryDetailView
)

urlpatterns = [
    # Список всех книг
    path('', BookListView.as_view(), name='book-list'),
    
    # Детальная страница книги: GET /api/books/1/
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Детальная страница категории: GET /api/books/categories/1/
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Детальная страница автора: GET /api/books/authors/1/
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]