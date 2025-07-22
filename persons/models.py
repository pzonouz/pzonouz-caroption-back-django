from django.db import models

from core.models import TimeStampedModel


class Person(TimeStampedModel):
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True)
