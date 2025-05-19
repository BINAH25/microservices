from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .producer import publish
from .serializers import ProductSerializer
import random
from opentelemetry import trace
from opentelemetry.trace import set_span_in_context

# Get the tracer
tracer = trace.get_tracer(__name__)

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        with tracer.start_as_current_span("list_products"):
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def create(self, request):
        with tracer.start_as_current_span("create_product"):
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        with tracer.start_as_current_span("retrieve_product"):
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

    def update(self, request, pk=None):
        with tracer.start_as_current_span("update_product"):
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(instance=product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            publish('product_updated', serializer.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        with tracer.start_as_current_span("delete_product"):
            product = Product.objects.get(id=pk)
            product.delete()
            publish('product_deleted', pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
