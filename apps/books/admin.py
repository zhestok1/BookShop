from django.contrib import admin
from apps.books.models import Category, Author, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_birth']
    search_fields = ['first_name', 'last_name']
    readonly_fields = []


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Колонки в таблице списка книг (самое главное)
    list_display = ['title', 'category', 'author', 'price', 'stock', 'is_active', 'created_at']
    
    # Редактируемые поля прямо из таблицы (удобно быстро менять цену/остаток)
    list_editable = ['price', 'stock', 'is_active']
    
    # Удобные фильтры справа
    list_filter = ['is_active', 'cover_type', 'category', 'publisher']
    
    # Быстрый поиск по названию, ISBN и имени автора
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    
    # Поля только для чтения
    readonly_fields = ['created_at']
    
    # Красивая группировка полей на странице редактирования книги
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'category', 'author', 'price', 'stock', 'is_active')
        }),
        ('Характеристики печатного издания', {
            'fields': ('isbn', 'publisher', 'pages_count', 'cover_type', 'weight_g'),
            'classes': ('collapse',),  # Можно сворачивать секцию
        }),
        ('Медиа и даты', {
            'fields': ('cover', 'created_at')
        }),
    )