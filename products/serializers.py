from products.models import Product
from rest_framework.serializers import ModelSerializer, StringRelatedField


class ProductSerializer(ModelSerializer):
    brand = StringRelatedField()

    class Meta:
        model = Product
        fields = "__all__"
