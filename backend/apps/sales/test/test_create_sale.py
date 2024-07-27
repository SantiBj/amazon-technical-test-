from rest_framework.test import APITestCase
from rest_framework import status
from ...products.services.query import create_product
from ...inventory.services.queries import create_inventory,create_warehouse
from django.urls import reverse
from ..models import Sales,Items_sales
from .queries_db import storage_procedure_proccess_sale
from ...services.execute_query import execute_query

class SaleCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        execute_query(storage_procedure_proccess_sale)
        cls.product = create_product()
        cls.warehouse = create_warehouse()
        cls.inventory_item = create_inventory(product=cls.product,warehouse=cls.warehouse,quantity=10)

    def create_sale(self,payload):
        return self.client.post(reverse("sale-create"),
                                data=payload,format="json")
    
    def test_create_sale_with_valid_data(self):
        valid_payload = {
            "items_sale":[
                {
                    "inventory_id":self.inventory_item.id,
                    "quantity":2
                }
            ]
        }

        response = self.create_sale(valid_payload)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.inventory_item.refresh_from_db()
        self.assertEqual(self.inventory_item.quantity,8)
        self.assertEqual(Sales.objects.count(),1)
        sale = Sales.objects.first()
        self.assertEqual(sale.total,self.product.price * 2)
        self.assertEqual(Items_sales.objects.count(),1)
        item_sale = Items_sales.objects.first()
        self.assertEqual(item_sale.product_inventory,self.inventory_item)
        self.assertEqual(item_sale.quantity,2)
        self.assertEqual(item_sale.price_product,self.product.price)
        self.assertEqual(item_sale.subtotal,self.product.price * 2)
        
    def test_create_sale_with_insufficient_inventory(self):
        invalid_payload = {
            "items_sale":[
                {
                    "inventory_id":self.inventory_item.id,
                    "quantity":20
                }
            ]
        }

        response = self.create_sale(invalid_payload)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough quantity for Inventory ID', response.data['error'])

    def test_create_sale_with_nonexistent_inventory(self):
        invalid_payload = {
            "items_sale": [
                {
                    "inventory_id": self.inventory_item.id,
                    "quantity": 2
                },
                {
                    "inventory_id": self.inventory_item.id + 1,
                    "quantity": 2
                }
            ]
        }
        response = self.create_sale(invalid_payload)
        self.assertIn('Inventory with', response.data['error'])