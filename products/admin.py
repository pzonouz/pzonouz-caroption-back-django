from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget()},
    }
