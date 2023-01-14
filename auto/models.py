from django.db import models


class Vehicle(models.Model):
    registration_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Номер регистрации")
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    mileage = models.PositiveIntegerField(verbose_name="Пробег")
    color = models.CharField(max_length=255, blank=True, null=True, verbose_name="Цвет")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="Дата покупки")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.registration_number}"
