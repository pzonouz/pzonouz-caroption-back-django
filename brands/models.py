from django.db import models

from core.models import TimeStampedModel


class Brand(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
