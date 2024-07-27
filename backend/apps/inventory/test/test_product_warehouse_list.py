from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Warehouses
from ...products.services.query import create_product
from ..services.queries import create_inventory

class ProductWarehouseListView(APITestCase):
    def setUp(self):
        self.product = create_product()
        self.warehouse1 = Warehouses.objects.create(name="Warehouse 1", location="Location 1")
        self.warehouse2 = Warehouses.objects.create(name="Warehouse 2", location="Location 2")
        self.inventory1 = create_inventory(self.product,self.warehouse1,20)
        self.inventory2 = create_inventory(self.product,self.warehouse2,30)

    def request_view(self,id):
        return self.client.get(reverse("product-warehouses", kwargs={'product_id': id}))
    
    def test_get_warehouses_with_product(self):
        response = self.request_view(self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "inventory_id": self.inventory1.id,
                "name": self.warehouse1.name,
                "location": self.warehouse1.location,
                "quantity_product": self.inventory1.quantity
            },
            {
                "inventory_id": self.inventory2.id,
                "name": self.warehouse2.name,
                "location": self.warehouse2.location,
                "quantity_product": self.inventory2.quantity
            }
        ]
        self.assertEqual(response.data['results'], expected_data)

    def test_get_warehouses_with_stock_no_product(self):
        response = self.request_view(500)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "product 500 not found.")