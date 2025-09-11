from rest_framework.serializers import ModelSerializer

from images.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "name", "image_url", "created", "updated", "products")
