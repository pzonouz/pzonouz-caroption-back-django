from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.models import TimeStampedModel
from entities.models import Entity

PEVGEOT_OLD_NAME = "PEVGEOT_OLD"


class Product(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    info = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    image_urls = ArrayField(
        models.CharField(max_length=500),  # each string up to 500 chars
        blank=True,
        default=list,
    )
    image_url = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0, null=True)
    price2 = models.IntegerField(default=0, null=True)
    price3 = models.IntegerField(default=0, null=True)
    main_product = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="derived_products",
        on_delete=models.SET_NULL,
    )
    entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=0)
    category = models.ForeignKey(
        "categories.Category", on_delete=models.PROTECT, null=True
    )
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
    generated = models.BooleanField(default=False)
    generatable = models.BooleanField(default=False)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        constraints = [
            models.UniqueConstraint(
                fields=["main_product", "entity"], name="unique_main_entity_product"
            )
        ]

    def __str__(self) -> str:
        return str(self.name)
