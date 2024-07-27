from django.db import models
from django.db.models import CheckConstraint,Q
from ..inventory.models import Inventory

class Sales(models.Model):
    total = models.DecimalField(max_digits=10,decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sales"
        verbose_name = "sale"
        verbose_name_plural = "sales"
        constraints = [
            CheckConstraint(check=Q(total__gt=0),name='total_greater_than_zero')
        ]
        indexes = [
            models.Index(fields=['creation_date'])
        ]

    def __str__(self) -> str:
        return f"Sale {self.id} by {self.user.username} on {self.creation_date}"
    
class Items_sales(models.Model):
    product_inventory = models.ForeignKey(Inventory,on_delete=models.RESTRICT)
    sale = models.ForeignKey(Sales,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_product = models.DecimalField(max_digits=8,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table = "items_sales"
        verbose_name = "items_sale"
        verbose_name_plural = "items_sales"
        constraints = [
            models.UniqueConstraint(fields=['product_inventory','sale'],name="unique_sale_product"),
            CheckConstraint(check=Q(quantity__gt=0), name='quantity_items_sales_greater_than_zero'),
            CheckConstraint(check=Q(price_product__gt=0),name='price_product_greater_than_zero'),
            CheckConstraint(check=Q(subtotal__gt=0),name='subtotal_greater_than_zero')
        ]
        indexes = [
            models.Index(fields=['sale']),
            models.Index(fields=['product_inventory'])
        ]

