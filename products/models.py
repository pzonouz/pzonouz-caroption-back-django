from django.db import models

from core.models import TimeStampedModel


class Product(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    info = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    count = models.IntegerField()
    category = models.ForeignKey("categories.Category", on_delete=models.PROTECT)
    advantages = models.ManyToManyField(
        "advantages.Advantage",
        related_name="products",
        blank=True,
    )
    disadvantages = models.ManyToManyField(
        "disadvantages.Disadvantage",
        related_name="products",
        blank=True,
    )
    brand = models.ForeignKey(
        "brands.Brand",
        related_name="products",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.name)
