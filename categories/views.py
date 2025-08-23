from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from categories.models import Category
from categories.serializers import CategorySerializer
from core.permissions import IsAdminUserOrReadOnly
from products.models import Product
from products.serializers import ProductSerializer


class ParentCategoryList(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True).order_by("order")
    serializer_class = CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Category.objects.all().order_by("order")
    serializer_class = CategorySerializer


def get_category_descendants(category):
    descendants = [category]
    for child in category.children.all():
        descendants += get_category_descendants(child)
    return descendants


def get_products_in_category(category_id):
    category = Category.objects.get(id=category_id)
    descendants = get_category_descendants(category)
    return Product.objects.filter(category__in=descendants)


@api_view(["GET"])
@permission_classes([AllowAny])
def products_in_category(request, pk):
    products = get_products_in_category(pk)
    serializer = ProductSerializer(products, many=True, context={"request": request})
    return Response(serializer.data)
