import pytz
from django.db import models


# Create your models here.
class BetterVehicle(models.Model):
    registration_number = models.CharField(
        max_length=255,
        verbose_name="Номер регистрации",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
    )
    brand = models.ForeignKey(
        "BetterBrand",
        on_delete=models.CASCADE,
        related_name="vehicles",
        verbose_name="Бренд",
    )
    enterprise = models.ForeignKey(
        "BetterEnterprise",
        on_delete=models.CASCADE,
        related_name="vehicles",
        verbose_name="Предприятие",
    )
    driver = models.ForeignKey(
        "BetterDriver",
        on_delete=models.CASCADE,
        related_name="vehicles",
        verbose_name="Водитель",
    )

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self) -> str:
        return f"{self.registration_number}"


class BetterBrand(models.Model):
    brand = models.CharField(
        max_length=255,
        verbose_name="Бренд",
        unique=True,
    )

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self) -> str:
        return self.brand


class BetterEnterprise(models.Model):
    TIMEZONES = tuple(zip(pytz.country_timezones["Ru"], pytz.country_timezones["Ru"]))

    name = models.CharField(
        max_length=255,
        verbose_name="Название предприятия",
    )
    city = models.CharField(
        max_length=255,
        verbose_name="Город",
    )
    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        default="UTC",
        verbose_name="Часовой пояс",
    )

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"

    def __str__(self) -> str:
        return self.name


class BetterDriver(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name="Имя",
    )
    second_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия",
    )
    salary = models.PositiveIntegerField(
        verbose_name="Зарплата, руб",
    )
    enterprise = models.ForeignKey(
        "BetterEnterprise",
        on_delete=models.CASCADE,
        related_name="drivers",
        verbose_name="Предприятие",
    )
    vehicle = models.ForeignKey(
        "BetterVehicle",
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
