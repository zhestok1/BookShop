from rest_framework import serializers
from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    # Выводим строковое представление или логин автора вместо простого ID
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'book', 'author', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'book', 'author', 'created_at', 'updated_at']