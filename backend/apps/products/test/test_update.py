from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Products
from ..serializers.response import ProductDetailSerializer

class ProductUpdateViewTest(APITestCase):
    def setUp(self):
        self.product = Products.objects.create(
            name="Original Product",
            description="Original Description",
            price=1500.00
        )

    def request_view(self, data):
        return self.client.patch(reverse('product-update', kwargs={'pk': self.product.id}), data, format='json')


    def test_update_product_success(self):
        updated_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 2000.00
        }

        response = self.request_view(updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, updated_data["name"])
        self.assertEqual(self.product.description, updated_data["description"])
        self.assertEqual(self.product.price, updated_data["price"])
        expected_response_data = ProductDetailSerializer(self.product).data
        self.assertEqual(response.data, expected_response_data)


    def test_update_product_invalid_data(self):
        invalid_data = {
            "name": "",
            "description": "Updated Description",
            "price": 500.00
        }
        response = self.request_view(invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("price", response.data)
