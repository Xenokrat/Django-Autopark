from django.contrib import admin

from .models import CarMileageReport, ReportData


class CarMileageReportAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(ReportData)
admin.site.register(CarMileageReport, CarMileageReportAdmin)
