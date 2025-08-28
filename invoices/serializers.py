from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from invoices.models import Invoice, InvoiceItem


class InvoiceItemSerializer(ModelSerializer):
    id = serializers.CharField(source="pk", read_only=True)
    productname = SerializerMethodField()

    def get_productname(self, obj):
        return obj.product.name

    def get_personname(self, obj):
        return obj.product.name

    class Meta:
        model = InvoiceItem
        read_only_fields = ("productname",)
        fields = (
            "id",
            "price",
            "count",
            "description",
            "product",
            "invoice",
            "discount",
        ) + read_only_fields


class InvoiceSerializer(ModelSerializer):
    personname = SerializerMethodField()
    invoiceitems = InvoiceItemSerializer(many=True, read_only=True)

    def get_personname(self, object):
        return object.person.lastname

    class Meta:
        model = Invoice
        read_only_fields = ("personname",)
        fields = (
            "id",
            "person",
            "status",
            "type",
            "total",
            "invoiceitems",
        ) + read_only_fields
