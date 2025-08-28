from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, StringRelatedField

from products.models import Product


class ProductSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    brand = StringRelatedField()
    main_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_main_product(self, obj):
        if obj.main_product:
            return ProductSerializer(obj.main_product, context=self.context).data
        return None
