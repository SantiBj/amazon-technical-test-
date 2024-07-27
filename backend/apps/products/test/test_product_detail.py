from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from decimal import Decimal
from ..models import Products


class ProductDetailTest(APITestCase):
    def setUp(self):
        self.product = Products.objects.create(
            name="Test Product",
            description="Test description",
            price=1500.0
        )

    def request_view(self, product_id):
        return self.client.get(reverse("product-detail", kwargs={"pk": product_id}))

    def test_retrieve_product_success(self):
        response = self.request_view(self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['description'], self.product.description)
        self.assertEqual(Decimal(response.data['price']), self.product.price)

    def test_retrieve_product_not_found(self):
        non_existent_id = 9999
        response = self.request_view(non_existent_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
