from django.db import models
from django.db.models import CheckConstraint,Q


class Products(models.Model):
    name = models.CharField(min,max_length=100,unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        verbose_name = "product"
        verbose_name_plural = "Products"
        constraints = [
            CheckConstraint(check=Q(price__gt=1000), name='price_greater_than_zero')
        ]
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self) -> str:
        return self.name
    
