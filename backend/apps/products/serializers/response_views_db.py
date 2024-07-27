from rest_framework import serializers
from ..views_db import ProductInventoryView

class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryView
        fields = ['product_id', 'product_name', 'product_description', 'product_price', 'total_quantity']
