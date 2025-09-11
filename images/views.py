from rest_framework.viewsets import ModelViewSet, ViewSet

from core.permissions import IsAdminUserOrReadOnly
from images.models import Image
from images.serializers import ImageSerializer


class ImageViewset(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
