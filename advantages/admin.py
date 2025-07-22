from django.contrib import admin

from advantages.models import Advantage


@admin.register(Advantage)
class AdvantagesAdmin(admin.ModelAdmin):
    pass
