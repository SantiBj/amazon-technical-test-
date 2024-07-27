from django.urls import path
from .views import (
    ProductCreateView,
    ProductUpdateView,
    ProductListView,
    ProductDetailView,
    ProductDetailByIdsView,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("inventory/", ProductDetailByIdsView.as_view(), name="product-inventory-relation"),
]
