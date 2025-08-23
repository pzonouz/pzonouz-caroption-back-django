from django.db import models

from core.models import TimeStampedModel


class Disadvantage(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name
