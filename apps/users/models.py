from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

class User(AbstractUser):
    
    phone = models.CharField(max_length=25, blank=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, verbose_name='О себе')
    
    verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name='Код подтверждения')
    code_created_at = models.DateTimeField(blank=True, null=True, verbose_name='Время создания кода')
    
    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
        
    def generate_verification_code(self):
        '''Генерация верификационного кода при регистрации'''
        
        code = ''.join(random.choice('0123456789', k=6))
        self.verification_code = code
        self.code_created_at = timezone.now()
        self.save(update_fields=['verification_code', 'code_created_at'])
        return code
    
    def is_code_valid(self, code):
        """Проверяет совпадение кода и его актуальность (не старше 2 минут)."""
        if not self.verification_code or not self.code_created_at:
            return False
            
        # Проверяем совпадение кода
        if self.verification_code != code:
            return False
            
        # Проверяем, прошло ли меньше 120 секунд (2 минут)
        time_elapsed = (timezone.now() - self.code_created_at).total_seconds()
        if time_elapsed > 120:
            return False
            
        return True
    
