from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Эндпоинты авторизации и пользователей
    path('api/v1/users/', include('apps.users.urls')),
    
    # Эндпоинты каталога книг
    path('api/v1/books/', include('apps.books.urls')),
    
    # Эндпоинты корзины
    path('api/v1/cart/', include('apps.cart.urls')),
    
    # Эндпоинты комментариев
    path('api/v1/comments/', include('apps.comments.urls')),
    
    # Эндпоинты платёжки
    path('api/v1/payments.', include('apps.payments.urls')),
]