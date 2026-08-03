from django.db import models
from django.conf import settings
from apps.books.models import Book

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает оплаты'
        PAID = 'paid', 'Оплачен'
        CANCELED = 'canceled', 'Отменен'
        COMPLETED = 'completed', 'Завершен'
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус'
    )
    total_amount = models.DecimalField(
        max_length=10,
        decimal_places=2,
        max_digits=10,
        default=0,
        verbose_name='Итоговая сумма'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ #{self.id} — {self.user.username} ({self.get_status_display()})"
    
class OrderItem(models.Model):
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Книга'
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена на момент покупки'
    )
    
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f"{self.quantity} x {self.book.title} (Заказ #{self.order.id})"
    
class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'В обработке'
        SUCCESS = 'success', 'Успешно'
        FAILED = 'failed', 'Ошибка'

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Заказ'
    )
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name='ID транзакции платежной системы'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name='Статус платежа'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"Платеж для Заказа #{self.order.id} [{self.get_status_status_display() if hasattr(self, 'get_status_status_display') else self.status}]"
    
    

