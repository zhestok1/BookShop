from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.comments.permissions import IsOwnerOrReadOnly


class BookCommentCreateView(generics.CreateAPIView):
    """
    POST /api/v1/comments/books/<book_id>/
    Создание нового комментария к книге.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Автоматически подставляем автора (из токена/сессии) 
        # и книгу (из URL-параметра book_id)
        serializer.save(
            author=self.request.user,
            book_id=self.kwargs.get('book_id')
        )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/v1/comments/<id>/ - Просмотр отзыва
    PUT/PATCH /api/v1/comments/<id>/ - Редактирование (только автор)
    DELETE /api/v1/comments/<id>/ - Удаление (только автор)
    """
    queryset = Comment.objects.select_related('author', 'book').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]