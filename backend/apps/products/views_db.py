from django.db import models

class ProductInventoryView(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_quantity = models.IntegerField()

    class Meta:
        managed = False 
        db_table = 'product_inventory_view' 
