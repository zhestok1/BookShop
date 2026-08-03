from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название категории')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
        
    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Фамилия')
    bio = models.TextField(blank=True, null=True, verbose_name='Биография')
    photo = models.ImageField(upload_to='authors_photos/', blank=True, null=True, verbose_name='Фото')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']
        
    @property
    def full_name(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name
        
    def __str__(self):
        return self.full_name


class Book(models.Model):
    COVER_HARD = 'hard'
    COVER_SOFT = 'soft'
    COVER_CHOICES = [
        (COVER_HARD, 'Твёрдый переплёт'),
        (COVER_SOFT, 'Мягкий переплёт'),
    ]

    title = models.CharField(max_length=500, verbose_name='Название книги')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='books',
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Автор'
    )
    
    # Цена и Остаток на складе
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток на складе (шт)')
    
    # Характеристики печатного издания
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='ISBN')
    publisher = models.CharField(max_length=255, blank=True, null=True, verbose_name='Издательство')
    pages_count = models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество страниц')
    cover_type = models.CharField(
        max_length=10, 
        choices=COVER_CHOICES, 
        default=COVER_HARD, 
        verbose_name='Тип переплёта'
    )
    weight_g = models.PositiveIntegerField(blank=True, null=True, verbose_name='Вес в граммах')
    
    # Медиа
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Обложка')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Доступна к продаже')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} (Остаток: {self.stock} шт)"
    
    @property
    def is_in_stock(self):
        """Быстрая проверка доступности книги к покупке"""
        return self.stock > 0 and self.is_active