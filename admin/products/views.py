from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .models import Product
from .producer import publish
from .serializers import ProductSerializer
import random

from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

# Initialize tracer
tracer = trace.get_tracer(__name__)

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        with tracer.start_as_current_span("list_products") as span:
            products = Product.objects.all()
            span.set_attribute("products.count", products.count())
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def create(self, request):
        with tracer.start_as_current_span("create_product") as span:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            product_data = serializer.data
            span.set_attribute("product.id", product_data.get("id"))
            span.set_attribute("product.title", product_data.get("title"))

            publish('product_created', product_data)
            return Response(product_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        with tracer.start_as_current_span("retrieve_product") as span:
            try:
                product = Product.objects.get(id=pk)
                span.set_attribute("product.id", product.id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                span.set_status(Status(StatusCode.ERROR, "Product not found"))
                return Response({"error": "Product not found"}, status=404)

    def update(self, request, pk=None):
        with tracer.start_as_current_span("update_product") as span:
            try:
                product = Product.objects.get(id=pk)
                serializer = ProductSerializer(instance=product, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                updated_data = serializer.data
                span.set_attribute("product.id", updated_data.get("id"))
                span.set_attribute("product.title", updated_data.get("title"))

                publish('product_updated', updated_data)
                return Response(updated_data, status=status.HTTP_202_ACCEPTED)
            except Product.DoesNotExist:
                span.set_status(Status(StatusCode.ERROR, "Product not found"))
                return Response({"error": "Product not found"}, status=404)

    def destroy(self, request, pk=None):
        with tracer.start_as_current_span("delete_product") as span:
            try:
                product = Product.objects.get(id=pk)
                product.delete()
                span.set_attribute("product.id", pk)
                publish('product_deleted', pk)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Product.DoesNotExist:
                span.set_status(Status(StatusCode.ERROR, "Product not found"))
                return Response({"error": "Product not found"}, status=404)


class UserAPIView(APIView):
    def get(self, _):
        with tracer.start_as_current_span("get_random_user") as span:
            users = User.objects.all()
            span.set_attribute("user.count", users.count())

            if not users:
                span.set_status(Status(StatusCode.ERROR, "No users found"))
                return Response({'error': 'No users available'}, status=404)

            user = random.choice(users)
            span.set_attribute("user.id", user.id)

            return Response({
                'id': user.id
            })