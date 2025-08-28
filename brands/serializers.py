from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from brands.models import Brand


class BrandSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    parent = serializers.CharField(source="parent_id", allow_null=True, required=False)

    class Meta:
        model = Brand
        fields = "__all__"
