from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products_catalog.models import Product
from products_catalog.serializers import ProductSerializer

from products_catalog.models import Category
from products_catalog.serializers import CategorySerializer


class ProductsView(APIView):
    """Получение товаров по категории"""

    def post(self, request):
        category = request.data.get('category')
        products = Product.objects.all().filter(category=category)
        if not products.exists():
            return Response({'error': 'Товаров в данной категории не существует'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)


class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
