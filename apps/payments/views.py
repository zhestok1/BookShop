from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.payments.models import Order, OrderItem, Payment
from apps.payments.serializers import OrderSerializer


class CheckoutView(APIView):
    """
    POST /api/v1/payments/checkout/
    Превращает текущую корзину пользователя в оформленный Order.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart = getattr(user, 'cart', None)

        if not cart or not cart.items.exists():
            return Response(
                {"detail": "Корзина пуста. Невозможно оформить заказ."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Все операции делаем в атомарном блоке, чтобы при ошибке ничего не сохранялось
        with transaction.atomic():
            cart_items = cart.items.select_related('book').all()

            # 1. Создаем заказ
            order = Order.objects.create(
                user=user,
                total_amount=0
            )

            total_amount = 0
            order_items_to_create = []

            # 2. Переносим товары из корзины в OrderItem
            for item in cart_items:
                item_total = item.book.price * item.quantity
                total_amount += item_total

                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        book=item.book,
                        price=item.book.price,  # Фиксируем цену на момент покупки!
                        quantity=item.quantity
                    )
                )

            # Массовая вставка товаров для оптимизации запросов к БД
            OrderItem.objects.bulk_create(order_items_to_create)

            # 3. Обновляем итоговую сумму заказа
            order.total_amount = total_amount
            order.save()

            # 4. Очищаем корзину
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """
    GET /api/v1/payments/orders/
    Список всех заказов текущего пользователя.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items__book', 'payment')
        )


class OrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/payments/orders/<id>/
    Детали конкретного заказа.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items__book', 'payment')
        )

class PayOrderView(APIView):
    """
    POST /api/v1/payments/orders/<id>/pay/
    Имитация оплаты заказа.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)

        if order.status == Order.Status.PAID:
            return Response({"detail": "Заказ уже оплачен."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем запись платежа и меняем статус заказа
        with transaction.atomic():
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'amount': order.total_amount,
                    'status': Payment.PaymentStatus.SUCCESS,
                    'transaction_id': f"TXN-{order.id}-{request.user.id}"
                }
            )
            order.status = Order.Status.PAID
            order.save()

        return Response(
            {"detail": "Оплата прошла успешно!", "order_id": order.id, "status": order.status},
            status=status.HTTP_200_OK
        )