from ..models import Products

def get_product(product_id:int)->list[Products]:
    return Products.objects.filter(id=product_id)

def create_product()->Products:
    return Products.objects.create(name="test product",description="test product",price=2000)