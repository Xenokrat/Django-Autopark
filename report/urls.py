from django.urls import path

from .views import CarMileageReportView, report_types

urlpatterns = [
    path("", report_types, name="report_types"),
    path("car-mileage-report", CarMileageReportView.as_view(), name="car_mileage_report"),
]
