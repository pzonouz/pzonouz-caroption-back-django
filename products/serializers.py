from inspect import Parameter

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from brands.models import Brand
from brands.serializers import BrandSerializer
from categories.models import Category
from categories.serializers import CategorySerializer
from parameters.models import ProductParameterValue
from parameters.serializers import ProductParameterValueSerializer
from products.models import Product


class ProductSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    brand = PrimaryKeyRelatedField(queryset=Brand.objects.all())
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    main_product = serializers.SerializerMethodField()
    category_full = CategorySerializer(source="category", read_only=True)
    parameter_values = ProductParameterValueSerializer(many=True)
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

    def update(self, instance, validated_data):
        # Pop nested values from data
        parameter_values_data = validated_data.pop("parameter_values", [])

        # Update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle parameter values (create or update)
        for pv_data in parameter_values_data:
            ProductParameterValue.objects.update_or_create(
                product=instance,
                parameter=pv_data["parameter"],
                defaults=pv_data,
            )

        return instance

    def get_main_product(self, obj):
        if obj.main_product:
            return ProductSerializer(obj.main_product, context=self.context).data
        return None
