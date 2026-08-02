from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    phone = models.CharField(max_length=25, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
        
    
    
