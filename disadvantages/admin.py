from django.contrib import admin

from disadvantages.models import Disadvantage


@admin.register(Disadvantage)
class DisadvantagesAdmin(admin.ModelAdmin):
    pass
