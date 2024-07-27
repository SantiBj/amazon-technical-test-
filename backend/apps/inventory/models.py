from django.db import models
from ..products.models import Products
from django.db.models import CheckConstraint,Q

class Warehouses(models.Model):
    name = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=255,unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "warehouses"
        verbose_name = "warehouse"
        verbose_name_plural = "warehouses"
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self) -> str:
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouses,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory"
        verbose_name = "inventory"
        verbose_name_plural = "inventory"
        constraints = [
            models.UniqueConstraint(fields=['product','warehouse'],name='unique_product_warehouse'),
            CheckConstraint(check=Q(quantity__gte=0), name='quantity_equal_greater_than_zero')
        ]
        indexes = [
            models.Index(fields=['product','warehouse']),
        ]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.warehouse.name}"