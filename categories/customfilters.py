from django.contrib import admin

from categories.models import Category


class ParentCategoryFilter(admin.SimpleListFilter):
    title = "Parent Category"
    parameter_name = "parent_category"

    def lookups(self, request, model_admin):
        parent_categories = Category.objects.filter(children__isnull=False).distinct()
        return [(cat.pk, cat.name) for cat in parent_categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__id=self.value())
        return queryset
