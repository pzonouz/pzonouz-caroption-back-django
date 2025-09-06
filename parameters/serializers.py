from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, StringRelatedField

from parameters.models import Parameter, ParameterGroup, ProductParameterValue


class ParametersSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = Parameter
        fields = "__all__"
        extra_kwargs = {
            "selectable_values": {"allow_empty": True},
        }


class ParameterGroupsSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    category_name = StringRelatedField(source="category", read_only=True)
    category = serializers.CharField(source="category.pk", read_only=True)

    class Meta:
        model = ParameterGroup
        fields = ("id", "name", "category", "category_name")


class ProductParameterValueSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = ProductParameterValue
        fields = "__all__"
