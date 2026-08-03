from django.contrib import admin
from apps.comments.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    
    list_display = ['book', 'author', 'text', 'created_at', 'updated_at']
    search_fields = ['book__name', 'author__username']
    ordering = ['-updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
