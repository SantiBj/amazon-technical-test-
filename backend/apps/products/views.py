from .serializers.request import (
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductWarehouseListSerializer,
)
from .serializers.response import (
    ProductDetailSerializer,
    ProductInventoryDetailSerializer,
)
import logging
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.db import DatabaseError
from .models import Products
from .views_db import ProductInventoryView
from .serializers.response_views_db import ProductInventorySerializer
from .services.generated_consults import format_consult_create,format_get_product_inventory
from ..services.execute_procedures import execute_procedure

logger = logging.getLogger("apps.products")


class ProductCreateView(APIView):
    @extend_schema(
        request=ProductCreateSerializer,
        responses={
            201: ProductDetailSerializer,
            400: OpenApiResponse(response=dict, description="Invalid input data"),
            500: OpenApiResponse(response=dict, description="server error"),
        },
        summary="Create a new product",
        description="This endpoint allows you to create a new product. You need to provide the product's name, description, price, warehouse ID, and quantity.",
        tags=["Products"],
    )
    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            consult = format_consult_create(serializer)
            product_id = execute_procedure(consult)

            if not product_id:
                raise Exception("Product creation failed.")
            product = Products.objects.get(id=product_id)
            product_serializer = ProductDetailSerializer(product)
            logger.info("Product created with success.")
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)

        except DatabaseError as e:
            logger.error(f"error database in the creation : {e}")
            error_message = str(e)
            return Response(
                {"error": f"Database error: {error_message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"error in the creation : {e}")
            return Response(
                {"error": f"An unexpected error ocurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductUpdateSerializer

    @extend_schema(
        request=ProductUpdateSerializer,
        responses={
            200: ProductDetailSerializer,
            400: OpenApiResponse(response=dict, description="Invalid input data"),
            500: OpenApiResponse(response=dict, description="server error"),
        },
        summary="Update product",
        description="This endpoint allows you to update a product. You need to provide the product's name, description and price.",
        tags=["Products"],
    )
    def patch(self, request, *args, **kwargs):
        try:
            super().patch(request, *args, **kwargs)
            product = self.get_object()
            response_data = ProductDetailSerializer(product).data
            logger.info("Product updated with success.")
            return Response(response_data, status=status.HTTP_200_OK)
        except DatabaseError as e:
            error_message = str(e)
            return Response(
                {"error": f"Database error: {error_message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(methods=["PUT"], exclude=True)
    def put(self, request, *args, **kwargs):
        return Response(
            {"error": "PUT method is not supported for this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class ProductListView(generics.ListAPIView):
    queryset = ProductInventoryView.objects.all()
    serializer_class = ProductInventorySerializer
    pagination_class = PageNumberPagination

    @extend_schema(
        responses={
            200: ProductInventorySerializer(many=True),
            400: OpenApiResponse(response=dict, description="Invalid request data"),
        },
        summary="List products with total quantity",
        description="This endpoint returns a paginated list of products along with the total quantity of each product.",
        tags=["Products"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductDetailSerializer

    @extend_schema(
        responses={
            200: ProductDetailSerializer,
            400: OpenApiResponse(response=dict, description="Product not found"),
        },
        summary="Retrieve a single product",
        description="Retrieves the details of a product by its ID.",
        tags=["Products"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailByIdsView(APIView):
    @extend_schema(
        request=ProductWarehouseListSerializer,
        responses={
            200: ProductInventoryDetailSerializer(many=True),
            400: OpenApiResponse(response=dict, description="Bad Request"),
        },
        summary="Details of each product of a sale",
        description="Retrieve product details based on provided product and warehouse IDs.",
        tags=["Products"],
    )
    def post(self, request):
        try:
            serializer = ProductWarehouseListSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            query = format_get_product_inventory(serializer)
            response_data = execute_procedure(query)
            
            if isinstance(response_data, dict):
                details = response_data.get('details', [])
                missing_ids = response_data.get('missing_ids', [])
                if missing_ids:
                    logger.warning(f"Missing IDs: {missing_ids}")
            else:
                details = response_data

            inventory_serializer = ProductInventoryDetailSerializer(details, many=True)
            return Response(inventory_serializer.data, status=status.HTTP_200_OK)
        
        except DatabaseError as e:
            error_message = str(e)
            return Response(
                {"error": f"Database error: {error_message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

