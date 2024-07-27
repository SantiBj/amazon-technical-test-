from rest_framework import serializers
from ..models import Warehouses

class WarehouseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouses
        fields = ["id","name","location"]

class WarehouseStockSerializer(serializers.Serializer):
    inventory_id= serializers.IntegerField()
    name= serializers.CharField()
    location = serializers.CharField()
    quantity_product = serializers.IntegerField()
    