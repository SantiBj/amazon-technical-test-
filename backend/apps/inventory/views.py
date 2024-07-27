from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .models import Warehouses
from .serializers.warehouses_response_serializers import (
    WarehouseStockSerializer,
    WarehouseDetailsSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from .services.queries import get_stock_of_product_warehouses,find_warehouses_with_stock
from ..products.services.query import get_product
from .exceptions.NotFoundException import NotFoundException
from rest_framework.response import Response


class WarehousesListView(generics.ListAPIView):
    queryset = Warehouses.objects.all().order_by("-creation_date")
    serializer_class = WarehouseDetailsSerializer
    pagination_class = None

    @extend_schema(
        responses={
            200: WarehouseDetailsSerializer(many=True),
            400: OpenApiResponse(response=dict, description="Invalid request data"),
        },
        summary="List of warehouses.",
        description="This endpoint returns a paginated list of warehouses.",
        tags=["Inventory"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProducWarehouseListView(APIView):
    class Pagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = "page_size"
        max_page_size = 100

    @extend_schema(
        responses={
            200: WarehouseStockSerializer(many=True),
            400: OpenApiResponse(response=dict, description="Invalid request data"),
            500: OpenApiResponse(response=dict, description="internal server error"),
        },
        summary="warehouses with stock of a product.",
        description="list of wineries that store a specific product, with the quantity of stocks of this product in each winery.",
        tags=["Inventory"],
    )
    def get(self, request, product_id, *args, **kwargs):
        try:
            product = get_product(product_id)
            if len(product) == 0:
                raise NotFoundException(f"product {product_id} not found.")
            stocks = get_stock_of_product_warehouses(product_id)
            paginator = self.Pagination()
            paginated_stocks = paginator.paginate_queryset(stocks, request)
            serializer = WarehouseStockSerializer(paginated_stocks, many=True)
            return paginator.get_paginated_response(serializer.data)
        except NotFoundException as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"internal server error": f"{e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        

class WarehousesWithStockProductListView(APIView):
    @extend_schema(
        responses={
            200: WarehouseStockSerializer(many=True),
            400: OpenApiResponse(response=dict, description="Invalid request data"),
            500: OpenApiResponse(response=dict, description="internal server error"),
        },
        summary="List of warehouses with stock of a product.",
        description="List of warehouses with stock of a product.",
        tags=["Inventory"],
    )
    def get(self, request, product_id, *args, **kwargs):
        try:
            product = get_product(product_id)
            if len(product) == 0:
                raise NotFoundException(f"product {product_id} not found.")
            stocks = find_warehouses_with_stock(product_id)
            serializer = WarehouseStockSerializer(stocks, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except NotFoundException as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"internal server error": f"{e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# relacion de bodega con producto con un cantidad de existencias (opcional)
