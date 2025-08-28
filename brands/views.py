from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from brands.models import Brand
from brands.serializers import BrandSerializer


class BrandsViewset(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    ordering = ("name",)
