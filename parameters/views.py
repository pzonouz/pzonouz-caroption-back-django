from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["parameter_group"]


class ParameterGroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = ParameterGroup.objects.all()
    serializer_class = ParameterGroupsSerializer


class ProductParameterValueViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = ProductParameterValue.objects.all()
    serializer_class = ProductParameterValueSerializer


@api_view(["GET"])
def getProductParameterValuesByProduct(request, id):
    values = ProductParameterValue.objects.filter(product__id=id)
    return Response(
        ProductParameterValueSerializer(values, many=True).data, status=HTTP_200_OK
    )
