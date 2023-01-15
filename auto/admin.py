from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        "id",
        "registration_number",
        "VIN",
        "year",
        "cost",
        "mileage",
        "color",
        "purchase_date",
        "get_photo",
    )
    list_display_links = (
        "id",
        "registration_number",
        "VIN",
    )
    search_fields = ("registration_number",)
    readonly_fields = ("get_photo",)
    fields = (
        "registration_number",
        "VIN",
        "year",
        "cost",
        "mileage",
        "color",
        "purchase_date",
        "photo",
        "get_photo",
    )

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="200">')
        return "-"

    get_photo.short_description = "Изображение"


admin.site.register(Vehicle, VehicleAdmin)
