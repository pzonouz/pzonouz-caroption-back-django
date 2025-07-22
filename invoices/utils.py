# utils/invoice.py or services/invoice_service.py

from .models import Invoice, InvoiceItem


def add_item_to_invoice(
    invoice: Invoice, product, price, count, discount=0, description=None
):
    item, created = InvoiceItem.objects.get_or_create(
        invoice=invoice,
        product=product,
        defaults={
            "price": price,
            "count": count,
            "discount": discount,
            "description": description,
        },
    )

    if not created:
        item.count += count
        item.save(update_fields=["count"])

    # Recalculate total:
    invoice.total = sum(
        (i.price * i.count) - i.discount for i in invoice.invoiceitems.all()
    )
    invoice.save(update_fields=["total"])

    return item
