from rest_framework import serializers
from django.core.validators import MinValueValidator

class ItemsSaleSerializer(serializers.Serializer):
    inventory_id = serializers.IntegerField(validators=[MinValueValidator(1)],help_text="product relationship warehouse.")
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)])

class SaleCreateSerializer(serializers.Serializer):
    items_sale = ItemsSaleSerializer(many=True)
