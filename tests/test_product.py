import random
import faker_commerce
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.helpers import STATE_NAMES
from bangazon_api.models import Category
from bangazon_api.models import Product, Order


class ProductTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=2)
        self.user1 = User.objects.filter(store__isnull=False).first()
        self.token = Token.objects.get(user=self.user1)

        self.product = Product.objects.first()
        self.order1 = Order.objects.first()

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        category = Category.objects.first()

        data = {
            "name": self.faker.ecommerce_name(),
            "price": random.randint(50, 1000),
            "description": self.faker.paragraph(),
            "quantity": random.randint(2, 20),
            "location": random.choice(STATE_NAMES),
            "imagePath": "",
            "categoryId": category.id
        }
        response = self.client.post('/api/products', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])

    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        product = Product.objects.first()
        data = {
            "name": product.name,
            "price": product.price,
            "description": self.faker.paragraph(),
            "quantity": product.quantity,
            "location": product.location,
            "imagePath": "",
            "categoryId": product.category.id
        }
        response = self.client.put(
            f'/api/products/{product.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        product_updated = Product.objects.get(pk=product.id)
        self.assertEqual(product_updated.description, data['description'])

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())

    def test_cannot_add_product_to_closed_order(self):
        """Ensures that a user cannot add a new product to an order that is already closed"""
        response = self.client.post(
            f'/api/products/{self.product.id}/add_to_order')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_product(self):
        response = self.client.delete(f'/api/products/{self.product.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_rating_to_product(self):
        product_unrated = self.product
        url = f'/api/products/{product_unrated.id}/rate-product'
        data = {
            "score": 7,
            "review": "This is a review, my guy"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product_rated = self.client.get(f'/api/products/{product_unrated.id}')

        self.assertEqual(len(product_rated.data['ratings']), 2)

        def average_rating():
            total_rating = 0
            num_of_ratings = len(product_rated.data['ratings'])
            avg = 0

            if num_of_ratings != 0:
                for rating in product_rated.data['ratings']:
                    total_rating += rating['score']

                avg = total_rating / num_of_ratings
            return avg

        avg = average_rating()

        self.assertEqual(product_rated.data['average_rating'], avg)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
