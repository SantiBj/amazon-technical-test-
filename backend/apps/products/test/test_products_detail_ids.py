from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ...inventory.services.queries import create_warehouse,create_inventory
from ..models import Products
from .services.queries_db import get_product_cart
from ...services.execute_query import execute_query

class ProductDetailByIdsViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        execute_query(get_product_cart)

    def setUp(self):
        self.product1 = Products.objects.create(
            name="Product 1",
            description="Description 1",
            price=1500.00
        )
        self.product2 = Products.objects.create(
            name="Product 2",
            description="Description 2",
            price=2000.00
        )
        self.warehouse1 = create_warehouse()
        self.warehouse2 = create_warehouse(2)
        

        self.inventory1 = create_inventory(
            product=self.product1,
            warehouse=self.warehouse1,
            quantity=10
        )
        self.inventory2 = create_inventory(
            product=self.product1,
            warehouse=self.warehouse2,
            quantity=20
        )

    def request_view(self, data):
        return self.client.post(reverse("product-inventory-relation"), data, format='json')

    def test_get_product_details_success(self):
        data = {
            "products_ids": [self.inventory1.id, self.inventory2.id]
        }
        response = self.request_view(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)