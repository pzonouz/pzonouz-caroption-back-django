from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminUserOrReadOnly
from products.models import Product
from products.serializers import ProductSerializer


class ProductsViewset(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering_fields = ("name",)
    ordering = ("name",)
