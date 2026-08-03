from django.urls import path
from apps.comments.views import BookCommentCreateView, CommentDetailView

urlpatterns = [
    # POST /api/v1/comments/books/<book_id>/ — оставить отзыв к конкретной книге
    path('books/<int:book_id>/', BookCommentCreateView.as_view(), name='book-comment-create'),
    
    # GET/PUT/PATCH/DELETE /api/v1/comments/<id>/ — работать с конкретным отзывом по его ID
    path('<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]