from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = SerializerMethodField()
    parent_name = SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
