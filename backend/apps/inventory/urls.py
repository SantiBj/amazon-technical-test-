from django.urls import path
from .views import WarehousesListView, ProducWarehouseListView,WarehousesWithStockProductListView

urlpatterns = [
    path("warehouses/", WarehousesListView.as_view(), name="warehouses-list"),
    path(
        "product-warehouses/<int:product_id>/",
        ProducWarehouseListView.as_view(),
        name="product-warehouses",
    ),
    path(
        "warehouses-with-stock-product/<int:product_id>/",
        WarehousesWithStockProductListView.as_view(),
        name="warehouses-with-stock-product"
    )
]
