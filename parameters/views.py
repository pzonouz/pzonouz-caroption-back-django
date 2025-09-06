from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminUserOrReadOnly
from parameters.serializers import (
    ParameterGroupsSerializer,
    ParametersSerializer,
    ProductParameterValueSerializer,
)

from .models import Parameter, ParameterGroup, ProductParameterValue


class ParameterViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Parameter.objects.all()
    serializer_class = ParametersSerializer


class ParameterGroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = ParameterGroup.objects.all()
    serializer_class = ParameterGroupsSerializer


class ProductParameterValueViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = ProductParameterValue.objects.all()
    serializer_class = ProductParameterValueSerializer
