from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ...inventory.services.queries import create_warehouse,create_inventory,delete_all_inventory
from ..models import Products
from rest_framework.pagination import PageNumberPagination
from .services.queries_db import create_view
from ...services.execute_query import execute_query

class ProductListViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        execute_query(create_view)
        cls.product1 = Products.objects.create(
            name="Product 1",
            description="Description 1",
            price=1500.00
        )
        cls.product2 = Products.objects.create(
            name="Product 2",
            description="Description 2",
            price=2000.00
        )
        cls.warehouse1 = create_warehouse()
        cls.warehouse2 = create_warehouse(2)
        
        cls.inventory1 = create_inventory(
            product=cls.product1,
            warehouse=cls.warehouse1,
            quantity=10
        )
        cls.inventory2 = create_inventory(
            product=cls.product1,
            warehouse=cls.warehouse2,
            quantity=20
        )
        cls.inventory3 = create_inventory(
            product=cls.product2,
            warehouse=cls.warehouse1,
            quantity=15
        )

    def request_view(self, params=None):
        return self.client.get(reverse("product-list"), data=params)

    def test_get_product_list_success(self):
        response = self.request_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        expected_data = [
            {
                "product_id": self.product1.id,
                "product_name": self.product1.name,
                "product_description": self.product1.description,
                "product_price": "{:.2f}".format(self.product1.price),  
                "total_quantity": self.inventory1.quantity + self.inventory2.quantity
            },
            {
                "product_id": self.product2.id,
                "product_name": self.product2.name,
                "product_description": self.product2.description,
                "product_price": "{:.2f}".format(self.product2.price),  
                "total_quantity": self.inventory3.quantity
            }
        ]
        
        results = response.data['results']
        expected_data_sorted = sorted(expected_data, key=lambda x: x['product_id'])
        results_sorted = sorted(results, key=lambda x: x['product_id'])
        self.assertEqual(expected_data_sorted, results_sorted)

    def test_get_product_list_no_products(self):
        Products.objects.all().delete()
        delete_all_inventory()
        
        response = self.request_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_get_product_list_pagination(self):
        for i in range(5, 15):
            Products.objects.create(
                name=f"Product {i}",
                description=f"Description {i}",
                price=1000.00 + i
            )
        
        response = self.request_view(params={'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('next', response.data)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

        page_size = PageNumberPagination().page_size
        self.assertTrue(len(response.data['results']) <= page_size)