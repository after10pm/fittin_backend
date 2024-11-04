from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=serializer.validated_data['product'])
            if not created:
                cart_item.quantity += serializer.validated_data['quantity']
                cart_item.save()
                return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
            else:
                cart_item.quantity = serializer.validated_data['quantity']
                cart_item.save()
                return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data['product_id']
        items = cart.items.all()
        try:
            cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                serializer = CartItemSerializer(items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data['product_id']
        quantity = request.data['quantity']

        try:
            cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

