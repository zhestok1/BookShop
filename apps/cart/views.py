from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart, CartItem
# Исправили опечатку в имени сериализатора
from apps.cart.serializers import CartSerializer, AddToCartSerializer


class CartDetailView(APIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Вспомогательный метод для получения корзины текущего пользователя"""
        cart, _ = Cart.objects.select_related('user').prefetch_related(
            'items__book'
        ).get_or_create(user=self.request.user)
        return cart

    def get(self, request):
        """Просмотр содержимого корзины"""
        cart = self.get_object()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def post(self, request):
        """Добавление товара в корзину (или увеличение количества)"""
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']

        cart = self.get_object()

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Повторно подтягиваем корзину, чтобы пересчитать items и total_price
        cart = self.get_object()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def delete(self, request):
        """Удаление конкретного товара по book_id или полная очистка корзины"""
        cart = self.get_object()
        book_id = request.query_params.get('book_id') or request.data.get('book_id')

        if book_id:
            item = get_object_or_404(CartItem, cart=cart, book_id=book_id)
            item.delete()
        else:
            cart.items.all().delete()

        cart = self.get_object()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)