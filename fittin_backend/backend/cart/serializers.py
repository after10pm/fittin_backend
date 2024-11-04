from rest_framework import serializers

from cart.models import CartItem
from products_catalog.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']
