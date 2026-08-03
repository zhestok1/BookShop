from django.db import models
from django.conf import settings
from apps.books.models import Book

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Cart of {self.user.email}'
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'book')
        
    @property
    def total_price(self):
        return self.book.price * self.quantity
    

    
    