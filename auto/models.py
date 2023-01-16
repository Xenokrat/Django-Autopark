import re

from django.core.exceptions import ValidationError
from django.db import models


class Vehicle(models.Model):
    model = models.ForeignKey(
        "CarModel", related_name="car_model", on_delete=models.CASCADE, default=2, verbose_name="Бренд"
    )
    registration_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Номер регистрации")
    VIN = models.CharField(max_length=17, unique=True)
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    mileage = models.PositiveIntegerField(verbose_name="Пробег")
    color = models.CharField(max_length=255, blank=True, null=True, verbose_name="Цвет")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="Дата покупки")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.registration_number}"

    def clean(self):
        regex = "^\w*$"

        VIN = self.VIN.upper()
        if len(VIN) != 17 or not re.search(regex, VIN):
            raise ValidationError("Идентификатор VIN должен состоять из 17 символов, включая только буквы и цифры")

        reg_number = self.registration_number
        if not re.search(regex, reg_number):
            raise ValidationError("Номер регистрации должен состоять только из цифр и букв")


class CarModel(models.Model):
    brand = models.CharField(max_length=255, verbose_name="Бренд", unique=True)
    car_type = models.CharField(max_length=255, verbose_name="Тип авто")
    load_capacity = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Грузоподъемность, кг"
    )
    seats_number = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Количество мест")
    fuel_tank_volume = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Объем бака, куб.см"
    )
    drive_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тип привода")
    max_speed = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Максимальная скорость, км/ч")

    class Meta:
        verbose_name = "Бренд авто"
        verbose_name_plural = "Бренды авто"

    def __str__(self):
        return self.brand
