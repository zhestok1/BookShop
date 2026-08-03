# 📚 BookShop — Полная документация проекта

> **Bookstore REST API**  
> Высокопроизводительный модульный бэкенд интернет-магазина книг на Django REST Framework.

---

## 1. Общее описание проекта

**BookShop** — это полноценный REST API бэкенд для интернет-магазина книг.  
Проект построен по модульной архитектуре Django (apps) и реализует:

- JWT-аутентификацию с верификацией email
- Каталог книг (категории, авторы, фильтры, поиск, сортировка)
- Корзину с автоматическим созданием через Django Signals
- Систему комментариев/отзывов
- Транзакционно-безопасный Checkout (оформление заказа)
- Имитацию оплаты
- Расширенную админ-панель Django
- CORS для фронтенда (Vite/React и т.д.)

**Язык интерфейса и данных:** русский  
**Часовой пояс:** Europe/Moscow  
**База данных по умолчанию:** SQLite

---

## 2. Технологический стек

| Компонент                        | Версия / Библиотека              |
|----------------------------------|----------------------------------|
| Python                           | 3.12+                            |
| Django                           | 6.0.7                            |
| Django REST Framework            | 3.17.1                           |
| djangorestframework-simplejwt    | 5.5.1                            |
| django-cors-headers              | 4.9.0                            |
| django-filter                    | 26.1                             |
| Pillow                           | 12.3.0                           |
| asgiref                          | 3.12.1                           |
| PyJWT                            | 2.13.0                           |
| sqlparse                         | 0.5.5                            |
| tzdata                           | 2026.3                           |

---

## 3. Структура проекта (полное дерево)
BookShop/
│
├── apps/                          # Все приложения проекта
│   ├── users/                     # Пользователи + JWT + верификация
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py              # Кастомная модель User
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── books/                     # Каталог книг
│   │   ├── init.py
│   │   ├── admin.py               # Богатая админка
│   │   ├── apps.py
│   │   ├── filters.py             # django-filter
│   │   ├── models.py              # Category, Author, Book
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── cart/                      # Корзина
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── apps.py                # ready() → импорт signals
│   │   ├── models.py              # Cart + CartItem
│   │   ├── serializers.py
│   │   ├── signals.py             # Автосоздание корзины
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── comments/                  # Отзывы к книгам
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── permissions.py         # IsOwnerOrReadOnly
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   └── payments/                  # Заказы и платежи
│       ├── init.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py              # Order, OrderItem, Payment
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py               # Checkout + PayOrder
│       ├── tests.py
│       └── migrations/
│
├── config/                        # Конфигурация Django
│   ├── init.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py                    # Главный роутер
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── .gitignore
