from rest_framework.decorators import api_view
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminUserOrReadOnly
from products.models import Product
from products.serializers import ProductSerializer
from products.utils import sync_entity_products


class ProductsViewset(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering_fields = ("name",)
    ordering = ("name",)


@api_view(["POST"])
def generate_products(request):
    sync_entity_products()
    return Response({"status": "ok"})
