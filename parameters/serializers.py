from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, StringRelatedField

from categories.models import Category
from parameters.models import Parameter, ParameterGroup, ProductParameterValue
from products.models import Product


class StringPKRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return str(value.pk)


class ParametersSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    parameter_group = StringPKRelatedField(queryset=ParameterGroup.objects.all())

    class Meta:
        model = Parameter
        fields = ("id", "name", "field_type", "selectable_values", "parameter_group")

        extra_kwargs = {
            "selectable_values": {"allow_empty": True},
        }


class ParameterGroupsSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    category_name = StringRelatedField(source="category", read_only=True)
    category = StringPKRelatedField(queryset=Category.objects.all())
    parameters = ParametersSerializer(many=True, read_only=True)

    class Meta:
        model = ParameterGroup
        fields = ("id", "name", "category", "category_name", "parameters")

    def create(self, validated_data):
        parameter_group = ParameterGroup.objects.create(**validated_data)
        return parameter_group


class ProductParameterValueSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    parameter = StringPKRelatedField(queryset=Parameter.objects.all())
    product = StringPKRelatedField(queryset=Product.objects.all())

    def create(self, validated_data):
        product = validated_data["product"]
        parameter = validated_data["parameter"]

        # check if already exists
        instance = ProductParameterValue.objects.filter(
            product=product, parameter=parameter
        ).first()

        if instance:
            # Option A: raise error
            # raise serializers.ValidationError(
            #     {"detail": "This product already has a value for this parameter."}
            # )

            # Option B (instead of error): update existing
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance

        return super().create(validated_data)

    class Meta:
        model = ProductParameterValue
        fields = [
            "id",
            "bool_value",
            "parameter",
            "product",
            "selectable_value",
            "text_value",
        ]


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ("id", "name", "field_type", "selectable_values", "values")
