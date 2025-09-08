from django.contrib.postgres.fields import ArrayField
from django.db import models

parameter_choices = (("TX", "TEXT"), ("BL", "BOOLEAN"), ("SL", "SELECTABLE"))


class ParameterGroup(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "categories.Category", on_delete=models.CASCADE, related_name="parameter_groups"
    )


class Parameter(models.Model):
    name = models.CharField(max_length=255)
    parameter_group = models.ForeignKey(
        ParameterGroup, on_delete=models.CASCADE, related_name="parameters"
    )
    field_type = models.CharField(max_length=2, choices=parameter_choices)
    selectable_values = ArrayField(
        models.CharField(max_length=300), null=True, blank=True, default=list
    )


class ProductParameterValue(models.Model):
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="parameter_values"
    )
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, related_name="values"
    )
    text_value = models.CharField(max_length=200, null=True, blank=True)
    bool_value = models.BooleanField(null=True, blank=True)
    selectable_value = models.CharField(max_length=300, null=True, blank=True)
    constraints = [
        models.UniqueConstraint(
            fields=["product", "parameter"], name="unique_product_parameter"
        )
    ]

    def __str__(self):
        return f"{self.product.name} - {self.parameter.name}: {self.text_value or self.bool_value}"
