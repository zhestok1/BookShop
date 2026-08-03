from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Эндпоинты авторизации и пользователей
    path('api/v1/users/', include('apps.users.urls')),
    
    # Эндпоинты каталога книг
    path('api/v1/books/', include('apps.books.urls')),
]