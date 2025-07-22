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
        existing_item = (
            self.invoice.invoiceitems.filter(product=self.product)
            .exclude(pk=self.pk)
            .first()
        )
        if existing_item:
            existing_item.count += self.count
            existing_item.save(update_fields=["count"])

            # Update total
            item_total = self.count * self.price
            self.invoice.total += item_total
            self.invoice.save(update_fields=["total"])
            return

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            item_total = self.count * self.price
            self.invoice.total += item_total
            self.invoice.save(update_fields=["total"])

    def delete(self, *args, **kwargs):
        print(self)
        self.invoice.total -= self.count * self.price
        self.invoice.save(update_fields=["total"])
        return super().delete(*args, **kwargs)
