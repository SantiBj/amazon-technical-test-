from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers.request import SaleCreateSerializer
from ..services.execute_query import execute_query
from .services.generated_consults import format_consult_process_sale
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
import logging

logger = logging.getLogger("apps.sales")

class SaleCreateView(APIView):
    @extend_schema(
        request=SaleCreateSerializer,
        responses={
            204:"not content response",
            400: OpenApiResponse(response=dict, description="Bad Request")
        },
        summary="Create sale",
        description="creation of a sale and inventory update according to the relationship id warehouse product in inventory.",
        tags=["Sales"]
    )
    def post(self,request):
        serializer = SaleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            consult = format_consult_process_sale(serializer)
            execute_query(consult)
            logger.info(f"You made a purchase with success.")
            return Response(status=status.HTTP_204_NO_CONTENT)
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

