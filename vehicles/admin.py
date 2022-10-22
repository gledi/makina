from django.contrib import admin

from .models import Vehicle, Photo


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        "make",
        "model",
        "year",
        "transmission",
    ]
    list_editable = ["year", "transmission"]
    list_filter = ["year", "transmission"]


# admin.site.register(Vehicle, VehicleAdmin)
