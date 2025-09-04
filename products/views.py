from rest_framework.decorators import api_view
from rest_framework.views import Response, status
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminUserOrReadOnly
from products.models import Product
from products.serializers import ProductSerializer
from products.utils import sync_entity_products, update_all_derived_products


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


@api_view(["POST"])
def update_generated_products(request):
    update_all_derived_products()
    return Response({"status": "ok"})


@api_view(["POST"])
def delete_from_image_urls(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Exception as e:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    image_name = request.data.get("image_name")
    if image_name not in product.image_urls:
        return Response(
            {"error": f"Image '{image_name}' not found in product image URLs."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    product.image_urls.remove(image_name)  # remove by value
    product.save()
    return Response(status=200)
