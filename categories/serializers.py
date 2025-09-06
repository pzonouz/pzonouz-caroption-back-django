from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from categories.models import Category
from parameters.models import ParameterGroup
from parameters.serializers import ParameterGroupsSerializer


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    parent = serializers.CharField(source="parent_id", allow_null=True, required=False)
    children = SerializerMethodField()
    parent_name = SerializerMethodField()
    parameter_groups = ParameterGroupsSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "image_url",
            "first_page",
            "order",
            "parent",
            "children",
            "parent_name",
            "parameter_groups",
        )

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None

    # from ChatGPT
    def update(self, instance, validated_data):
        parameter_groups_data = validated_data.pop("parameter_groups", None)

        # Update the category fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle parameter_groups if included
        if parameter_groups_data is not None:
            # Delete existing parameter groups
            instance.parameter_groups.all().delete()

            # Recreate from the request payload
            for pg in parameter_groups_data:
                ParameterGroup.objects.create(
                    category=instance,
                    name=pg.get("name"),
                )

        return instance
