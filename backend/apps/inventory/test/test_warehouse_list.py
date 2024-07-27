from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Warehouses
from ..serializers.warehouses_response_serializers import WarehouseDetailsSerializer



class WarehousesListViewTest(APITestCase):
    def setUp(self):
        Warehouses.objects.create(name="Warehouse 2", location="Location 2")

    def request_view(self):
        return self.client.get(reverse("warehouses-list"))
    

    def test_get_warehouses_list(self):
        response = self.request_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        warehouses = Warehouses.objects.all().order_by("-creation_date")
        serializer = WarehouseDetailsSerializer(warehouses, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_warehouses_list_no_warehouses(self):
        Warehouses.objects.all().delete()
        response = self.request_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])