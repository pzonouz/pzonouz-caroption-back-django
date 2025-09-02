from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, StringRelatedField

from brands.models import Brand
from categories.models import Category
from products.models import Product


class ProductSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    brand = PrimaryKeyRelatedField(queryset=Brand.objects.all())
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    main_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "info",
            "description",
            "price",
            "price2",
            "price3",
            "main_product",
            "image_url",
            "image_urls",
            "count",
            "advantages",
            "disadvantages",
            "brand",
            "generated",
            "generatable",
            "category",
        ]

    def get_main_product(self, obj):
        if obj.main_product:
            return ProductSerializer(obj.main_product, context=self.context).data
        return None
