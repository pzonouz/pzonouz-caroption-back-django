from django.db import models

from core.models import TimeStampedModel


class Image(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.CharField(max_length=255)
