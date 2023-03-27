import calendar

from django.contrib.contenttypes.fields import (ContentType, GenericForeignKey,
                                                GenericRelation)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone

from auto.models import Vehicle


class Report(models.Model):
    DAY = "день"
    MONTH = "месяц"
    YEAR = "год"
    PERIOD_CHOICES = (
        (DAY, ("День")),
        (MONTH, ("Месяц")),
        (YEAR, ("Год")),
    )

    report_type = models.CharField(max_length=50, verbose_name="Тип отчета")
    period = models.CharField(max_length=10, verbose_name="Временной период", choices=PERIOD_CHOICES)
    start_date = models.DateField(verbose_name="Начальная дата")
    end_date = models.DateField(verbose_name="Конечная дата")
    # result = models.ManyToManyField("ReportData", verbose_name="Результат")

    class Meta:
        ordering = ("-start_date", "-end_date")
        abstract = True

    def __str__(self) -> str:
        return f"{self.report_type} {self.period} {self.start_date} -- {self.end_date}"

    def clean(self) -> None:
        if self.start_date > self.end_date:
            raise ValidationError("Конечная дата не может быть меньше начальной")


class ReportData(models.Model):
    time = models.CharField(max_length=50)
    value = models.DecimalField("Показатель", decimal_places=2, max_digits=8)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["object_id"]


class CarMileageReport(Report):
    report_type = models.CharField(default="Отчет по пробегу за период", max_length=50, verbose_name="Тип отчета")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mileage_data = GenericRelation(
        ReportData,
        related_query_name="report_data",
    )

    class Meta:
        verbose_name = "Отчет по пробегу автомобиля за период"
        verbose_name_plural = "Отчеты по пробегу автомобиля за период"

    def __str__(self) -> str:
        return f"Пробег авто {self.vehicle} {self.period} {self.start_date} -- {self.end_date}"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.period == self.DAY:
            self._generate_daily_mileage()
        if self.period == self.MONTH:
            self._generate_monthly_mileage()

    def _generate_daily_mileage(self):
        rides = (
            self.vehicle.auto_rides.filter(start_date__gte=self.start_date, end_date__lte=self.end_date)
            .values("end_date")
            .annotate(mileage_sum=Sum("distance"))
            .order_by("end_date")
        )
        for day in rides:
            self.mileage_data.create(
                time=day["end_date"].strftime("%Y-%m-%d"),
                value=day["mileage_sum"],
            )

    def get_absolute_url(self):
        return reverse("car_miliage_report_api", kwargs={"pk": self.pk})

    def _generate_monthly_mileage(self):
        rides = (
            self.vehicle.auto_rides.filter(start_date__gte=self.start_date, end_date__lte=self.end_date)
            .values("end_date__month", "end_date__year")
            .annotate(mileage_sum=Sum("distance"))
            .order_by("end_date")
        )
        for i in rides:
            time = calendar.month_name[i["end_date__month"]] + " " + str(i["end_date__year"])
            value = i["mileage_sum"]
            self.mileage_data.create(time=time, value=value)
