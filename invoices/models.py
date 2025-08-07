from django.db import models

from core.models import TimeStampedModel


class Invoice(TimeStampedModel):
    invoiceTypeChoices = (("B", "buy"), ("S", "sell"))
    invoiceStatusChoices = (("D", "Draft"), ("C", "Confirmed"))
    person = models.ForeignKey(
        "persons.Person", on_delete=models.PROTECT, related_name="invoices"
    )
    type = models.CharField(choices=invoiceTypeChoices, max_length=1)
    status = models.CharField(choices=invoiceStatusChoices, default="D")
    description = models.TextField(null=True, blank=True)
    total = models.PositiveBigIntegerField(default=0)

    def recalculate_total(self):
        total = sum(item.price * item.count for item in self.invoiceitems.all())  # type: ignore
        self.total = total
        self.save(update_fields=["total"])


class InvoiceItem(models.Model):
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    discount = models.IntegerField(default=0)
    product = models.ForeignKey(
        "products.Product", related_name="product", on_delete=models.PROTECT
    )
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="invoiceitems"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.recalculate_total()

    def delete(self, *args, **kwargs):  # type: ignore
        super().delete(*args, **kwargs)
        self.invoice.recalculate_total()
