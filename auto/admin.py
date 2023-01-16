from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CarModel, Vehicle


class VehicleAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        "id",
        "model",
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
        "model",
        "registration_number",
        "VIN",
    )
    search_fields = ("registration_number",)
    readonly_fields = ("get_photo",)
    fields = (
        "model",
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


class CarModelAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        "id",
        "brand",
        "car_type",
        "load_capacity",
        "seats_number",
        "fuel_tank_volume",
        "drive_type",
        "max_speed",
    )
    list_display_links = (
        "id",
        "brand",
    )
    search_fields = ("brand",)
    fields = (
        "brand",
        "car_type",
        "load_capacity",
        "seats_number",
        "fuel_tank_volume",
        "drive_type",
        "max_speed",
    )


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CarModel, CarModelAdmin)
