from django.test import TestCase

from django.urls import reverse
from rest_framework import status

from fittin_backend.backend.products_catalog.models import Category, Product


class ProductsViewTests(TestCase):
    def setUp(self):
        # Создаем тестовую категорию
        self.category = Category.objects.create(name='Test Category')
        self.product1 = Product.objects.create(
            name='Product 1',
            description='Description 1',
            price=10.00,
            stock=100,
            category=self.category
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            description='Description 2',
            price=20.00,
            stock=50,
            category=self.category
        )
        self.url = reverse('products/')

    def test_get_products_by_category_success(self):
        """Тест успешного получения продуктов по категории"""
        response = self.client.post(self.url, {'category': self.category.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.product1.name)
        self.assertEqual(response.data[1]['name'], self.product2.name)

    def test_get_products_by_category_no_products(self):
        """Тест обработки случая, когда нет продуктов в категории"""
        new_category = Category.objects.create(name='Empty Category')
        response = self.client.post(self.url, {'category': new_category.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Товаров в данной категории не существует'})


class ProductDetailViewTests(TestCase):

    def setUp(self):
        # Создайте тестовые данные
        self.product = Product.objects.create(
            id=1,
            name='Test Product',
            description='A test product',
            price=100.00,
            stock=10,
            category=None,
            image='path/to/image.jpg',
            size='M',
            season='Summer',
            color='Red',
            fabric_type='Cotton',
            style='Casual',
            brand='Test Brand'
        )

    def test_get_product(self):
        url = reverse('product', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['description'], self.product.description)

    def test_get_non_existent_product(self):
        # Тестируем получение несуществующего продукта
        url = reverse('product-detail', kwargs={'pk': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Продукт не найден')
