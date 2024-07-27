from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Products
from ...inventory.services.queries import create_warehouse
from .services.queries_db import storage_procedure_proccess_create_product
from ...services.execute_query import execute_query

class ProductCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        execute_query(storage_procedure_proccess_create_product)


    def setUp(self):
        self.warehouse1 = create_warehouse()
        self.warehouse2 = create_warehouse(2)

    def request_view(self, data):
        return self.client.post(reverse("product-create"), data, format='json')

    def test_create_product_success(self):
        data = {
            "name": "New Product",
            "description": "A test product",
            "price": 1200.00,
            "warehouses": [
                {"warehouse_id": self.warehouse1.id, "quantity": 10},
                {"warehouse_id": self.warehouse2.id, "quantity": 20}
            ]
        }
        response = self.request_view(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Products.objects.filter(name="New Product").exists())

    def test_create_product_invalid_data(self):
        data = {
            "name": "NP",
            "description": "A test product",
            "price": 900.00,
            "warehouses": [
                {"warehouse_id": self.warehouse1.id, "quantity": 10}
            ]
        }
        response = self.request_view(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("price", response.data)

    def test_create_existing_product(self):
        Products.objects.create(name="Existing Product", description="Existing", price=1500.00)
        data = {
            "name": "Existing Product",
            "description": "Another test product",
            "price": 1300.00,
            "warehouses": [
                {"warehouse_id": self.warehouse1.id, "quantity": 10}
            ]
        }
        response = self.request_view(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("already exists", response.data["name"][0])

    def test_create_product_with_nonexistent_warehouse(self):
        data = {
            "name": "Product with bad warehouse",
            "description": "Another test product",
            "price": 1300.00,
            "warehouses": [
                {"warehouse_id": 999, "quantity": 10}
            ]
        }
        response = self.request_view(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
