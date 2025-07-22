from django.contrib import admin

from categories.customfilters import ParentCategoryFilter
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = (ParentCategoryFilter,)
