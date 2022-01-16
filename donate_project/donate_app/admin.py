from django.contrib import admin

from donate_app.models import (
    Institution,
)


@admin.register(Institution)
class OrderAdmin(admin.ModelAdmin):
    fields = ['__all__']
