from rest_framework import serializers
from ..models import Products

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','name','description','price']

class ProductInventoryDetailSerializer(serializers.Serializer):
    id_inventario = serializers.IntegerField(help_text="relationship between product and waterhouse")
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_description = serializers.CharField()
    product_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    warehouse_name = serializers.CharField()