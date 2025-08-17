import random

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    first_page = models.BooleanField(default=False)
    order = models.CharField(max_length=3)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)
