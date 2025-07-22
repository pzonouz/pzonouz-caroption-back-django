from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAdminUserOrReadOnly
from invoices.models import Invoice, InvoiceItem
from invoices.serializers import InvoiceItemSerializer, InvoiceSerializer


class InvoiceViewset(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceItemViewset(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
