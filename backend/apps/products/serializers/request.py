from rest_framework import serializers
from django.core.validators import MinValueValidator
from ..models import Products


class ProductWarehouseSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField(validators=[MinValueValidator(1)],help_text="ID of the warehouse.")
    quantity = serializers.IntegerField(help_text="stock in the warehouse.")

class ProductCreateSerializer(serializers.ModelSerializer):
    
    warehouses = ProductWarehouseSerializer(many=True, help_text="stock in the warehouses.")
    class Meta:
        model = Products
        fields = ['name','description','price','warehouses']

    def validate_name(self,value):
        value = str(value).strip()
        if len(value) < 5:
            raise serializers.ValidationError("the name of the product must contain at least 5 characters.")
        if len(value) > 100:
            raise serializers.ValidationError("The product name cannot be longer than 100 characters.")
        return value
    
    def validate_description(self,value):
        value = str(value).strip()
        if len(value) < 5:
            raise serializers.ValidationError("the description of the product must contain at least 5 characters.")
        if len(value) > 255:
            raise serializers.ValidationError("The product description cannot be longer than 255 characters.")
        return value
    
    def validate_price(self,value):
        if value <= 0:
            raise serializers.ValidationError("the price of the product must be a positive number")
        
        min_value = 1000

        if value < min_value:
            raise serializers.ValidationError(f"The price should be at least {min_value}.")
        return value
    
class ProductUpdateSerializer(ProductCreateSerializer):
    class Meta(ProductCreateSerializer.Meta):
        fields = ['name', 'description', 'price']

class ProductWarehouseListSerializer(serializers.Serializer):
    products_ids = serializers.ListField(
        child=serializers.IntegerField(validators=[MinValueValidator(1)]),
        allow_empty=False,
        help_text="List of products with inventory IDs."
    )