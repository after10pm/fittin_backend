from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.serializers import OrderSerializer

from cart.models import Cart

from order.models import OrderItem, Order


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()

        if not items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = Decimal('0.00')
        order_items = []

        for item in items:
            total_price += item.product.price * item.quantity
            order_item = OrderItem(product=item.product, quantity=item.quantity)
            order_items.append(order_item)

        order = Order(user=request.user, total_price=total_price)
        order.save()

        for order_item in order_items:
            order_item.order = order
            order_item.save()

        if order.items.count() == len(order_items):
            cart.items.all().delete()
            return Response({"order_id": order.id, "total_price": str(total_price)}, status=status.HTTP_201_CREATED)

        return Response({"error": "Failed to create order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
