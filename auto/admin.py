from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CarModel, Driver, Enterprise, Vehicle


class VehicleForm(forms.ModelForm):
    queryset = Vehicle.objects.get(pk=3)

    class Meta:
        model = Vehicle
        # fields = "__all__"
        fields = ("model",)


class DriverInline(admin.TabularInline):
    model = Driver
    extra = 0


class VehicleAdmin(admin.ModelAdmin):
    form = VehicleForm
    inlines = [DriverInline]
    list_display = (
        "id",
        "model",
        "registration_number",
        "VIN",
        "current_driver",
        "enterprise",
        "year",
        "cost",
        "get_photo",
    )
    list_editable = (
        "current_driver",
        "enterprise",
    )
    list_display_links = (
        "id",
        "model",
        "registration_number",
        "VIN",
    )
    search_fields = ("registration_number",)
    readonly_fields = ("get_photo",)
    # fields = (
    #     "model",
    #     "registration_number",
    #     "VIN",
    #     "current_driver",
    #     "enterprise",
    #     "cost",
    #     "mileage",
    #     "color",
    #     "purchase_date",
    #     "photo",
    #     "get_photo",
    # )

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


class EnterpriseAdmin(admin.ModelAdmin):
    inlines = [DriverInline]
    save_as = True
    list_display = (
        "id",
        "name",
        "city",
    )
    list_display_links = (
        "id",
        "name",
    )
    search_fields = ("name",)
    fields = (
        "name",
        "city",
    )


class DriverAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        "id",
        "first_name",
        "second_name",
        "salary",
        "driving_experience",
        "enterprise",
        "vehicle",
    )
    list_editable = ("vehicle",)
    list_display_links = (
        "id",
        "first_name",
        "second_name",
    )
    search_fields = (
        "first_name",
        "second_name",
        "enterprise",
    )
    fields = (
        "first_name",
        "second_name",
        "salary",
        "driving_experience",
        "enterprise",
        "vehicle",
    )


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Driver, DriverAdmin)
