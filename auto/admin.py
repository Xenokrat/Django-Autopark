from typing import Any

from django import forms
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import CarModel, Driver, Enterprise, Manager, Vehicle


class DriverInline(admin.TabularInline):
    model = Driver
    extra = 0


class VehicleAdmin(admin.ModelAdmin):
    save_as = True
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
    list_editable = ("enterprise",)
    list_filter = ("enterprise",)
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
        "current_driver",
        "enterprise",
        "cost",
        "mileage",
        "year",
        "color",
        "purchase_date",
        "photo",
        "get_photo",
    )

    # Driver.objects.filter(enterprise__in=user.manager.enterprises.all())

    # def formfield_for_foreignkey(self, db_field, request, **kwargs: Any):
    #     if db_field.name == "current_driver":
    #         kwargs["queryset"] = Driver.objects.filter(enterprise__in=request.user.manager.enterprise.all())
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="200">')
        return "-"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super(VehicleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, "manager"):
            return qs.filter(enterprise__in=request.user.manager.enterprise.all())
        return qs.none()

    get_photo.short_description = "Изображение"  # type: ignore


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

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, "manager"):
            return qs.filter(enterprise__in=request.user.manager.enterprise.all())
        return qs.none()


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

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, "manager"):
            return qs.filter(enterprise__in=request.user.manager.enterprise.all())
        return qs.none()


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Manager)
