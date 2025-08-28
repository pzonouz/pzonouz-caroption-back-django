from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from entities.models import Entity


class EntitySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    parent = serializers.CharField(source="parent_id", allow_null=True, required=False)
    children = SerializerMethodField()
    parent_name = SerializerMethodField()

    class Meta:
        model = Entity
        fields = "__all__"

    def get_children(self, obj):
        children = obj.children.all()
        return EntitySerializer(children, many=True).data

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
