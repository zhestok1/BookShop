from django.db import models
from apps.books.models import Book
from apps.users.models import User

class Comment(models.Model):
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True
    )
    
    text = models.TextField(blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-updated_at']
        
    def __str__(self):
        return self.text[:30]
    
    
    
