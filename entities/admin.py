from django.contrib import admin

from entities.models import Entity


@admin.register(Entity)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
