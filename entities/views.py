from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminUserOrReadOnly
from entities.models import Entity
from entities.serializers import EntitySerializer
from products.models import Product


class ParentEntityList(ListAPIView):
    queryset = Entity.objects.filter(parent__isnull=True).order_by("order")
    serializer_class = EntitySerializer


def get_entity_descendants(entity):
    descendants = [entity]
    for child in entity.children.all():
        descendants += get_entity_descendants(child)
    return descendants


def get_products_in_entity(entity_id):
    entity = Entity.objects.get(id=entity_id)
    descendants = get_entity_descendants(entity)
    return Product.objects.filter(entity__in=descendants)


class EntityViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Entity.objects.all().order_by("order")
    serializer_class = EntitySerializer
