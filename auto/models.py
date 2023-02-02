import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Manager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="manager", verbose_name="Учетная запись"
    )
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя")
    second_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Фамилия")
    enterprise = models.ManyToManyField("Enterprise", blank=True, verbose_name="Предприятия")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name}"


class Vehicle(models.Model):
    model = models.ForeignKey(
        "CarModel", related_name="vehicles", on_delete=models.CASCADE, default=2, verbose_name="Бренд"
    )
    registration_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Номер регистрации")
    VIN = models.CharField(max_length=17, unique=True)
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    mileage = models.PositiveIntegerField(verbose_name="Пробег")
    color = models.CharField(max_length=255, blank=True, null=True, verbose_name="Цвет")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="Дата покупки")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name="Фото")
    enterprise = models.ForeignKey(
        "Enterprise", on_delete=models.CASCADE, related_name="vehicles", null=True, verbose_name="Предприятие"
    )
    current_driver = models.OneToOneField(
        "Driver",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="vehicles",
        verbose_name="Активный водитель",
    )

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self) -> str:
        return f"{self.registration_number}"

    def validate_can_change_enterprise(self) -> None:
        if not self.pk:
            return
        vehicle = Vehicle.objects.get(pk=self.pk)
        if vehicle.enterprise != self.enterprise and self.current_driver:
            raise ValidationError(
                "Невозможно изменить предприятие для данного авто, так как ему назначен активный водитель"
            )

    def validate_current_driver_enterprise(self):
        if not self.current_driver:
            return
        if self.current_driver.enterprise != self.enterprise:
            raise ValidationError("Активный водитель должен быть из того же предприятия")

    def validate_vehicle_enterprise(self) -> None:
        if not self.pk:
            return
        vehicle = Vehicle.objects.get(pk=self.pk)
        if vehicle.enterprise == self.enterprise:
            return
        if self.enterprise.vehicles.filter(pk=self.pk).exists():
            raise ValidationError("Этот автомобиль уже принадлежит предприятию")

    def validate_vin(self) -> None:
        regex = "^\w*$"
        VIN = self.VIN.upper()
        if len(VIN) != 17 or not re.search(regex, VIN):
            raise ValidationError("Идентификатор VIN должен состоять из 17 символов, включая только буквы и цифры")

    def validate_reg_numbers(self) -> None:
        regex = "^\w*$"
        reg_number = self.registration_number
        if not re.search(regex, reg_number):
            raise ValidationError("Номер регистрации должен состоять только из цифр и букв")

    def clean(self) -> None:
        self.validate_can_change_enterprise()
        self.validate_current_driver_enterprise()
        self.validate_vehicle_enterprise()
        self.validate_vin()
        self.validate_reg_numbers()


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

    def __str__(self) -> str:
        return self.brand


class Driver(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    second_name = models.CharField(max_length=255, verbose_name="Фамилия")
    salary = models.PositiveIntegerField(blank=True, null=True, verbose_name="Зарплата, руб")
    driving_experience = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Водительский стаж")
    enterprise = models.ForeignKey(
        "Enterprise",
        on_delete=models.CASCADE,
        related_name="drivers",
        blank=True,
        null=True,
        verbose_name="Предприятие",
    )
    vehicle = models.ForeignKey(
        "Vehicle",
        on_delete=models.CASCADE,
        related_name="drivers",
        blank=True,
        null=True,
        verbose_name="Автомобиль",
    )

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name}"

    def validate_driver_enterprise(self):
        if not self.vehicle:
            return
        if self.vehicle.enterprise == self.enterprise:
            return
        raise ValidationError("Водитель должен быть из того же предприятия, что и авто")

    def clean(self) -> None:
        self.validate_driver_enterprise()


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название предприятия")
    city = models.CharField(max_length=255, verbose_name="Город")

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"

    def __str__(self) -> str:
        return self.name
