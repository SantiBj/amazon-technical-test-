from django.db.models import F
from ..models import Inventory,Warehouses


def create_warehouse(number:int=1):
    return Warehouses.objects.create(name=f"bodega test {number}",location=f"bogota {number}")

def create_inventory(product,warehouse,quantity:int)->Inventory:
    return Inventory.objects.create(product=product,warehouse=warehouse,quantity=quantity)

def delete_all_inventory():
    Inventory.objects.all().delete()

def get_stock_of_product_warehouses(product_id: int):
    stocks = (
        Inventory.objects.filter(product_id=product_id)
        .select_related("warehouse")
        .annotate(
            inventory_id=F("id"),
            name=F("warehouse__name"),
            location=F("warehouse__location"),
            quantity_product=F("quantity"),
        )
        .values("inventory_id", "name", "location", "quantity_product")
    )
    return list(stocks)

def find_warehouses_with_stock(product_id:int):
    stocks = (
        Inventory.objects.filter(product_id=product_id,quantity__gte=1)
        .select_related("warehouse")
        .annotate(
            inventory_id=F("id"),
            name=F("warehouse__name"),
            location=F("warehouse__location"),
            quantity_product=F("quantity"),
        )
        .values("inventory_id", "name", "location", "quantity_product")
    )
    return list(stocks)