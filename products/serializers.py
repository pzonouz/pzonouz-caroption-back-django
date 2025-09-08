from inspect import Parameter

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from brands.models import Brand
from brands.serializers import BrandSerializer
from categories.models import Category
from categories.serializers import CategorySerializer
from parameters.serializers import ProductParameterValueSerializer
from products.models import Product


class ProductSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    brand = PrimaryKeyRelatedField(queryset=Brand.objects.all())
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    main_product = serializers.SerializerMethodField()
    category_full = CategorySerializer(source="category", read_only=True)
    parameter_values = ProductParameterValueSerializer(many=True, read_only=True)
    brand_full = BrandSerializer(source="brand", read_only=True)

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
            "brand_full",
            "generated",
            "generatable",
            "category",
            "category_full",
            "parameter_values",
        ]

    def get_main_product(self, obj):
        if obj.main_product:
            return ProductSerializer(obj.main_product, context=self.context).data
        return None
