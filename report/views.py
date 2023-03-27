from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView

from .froms import CarMileageReportForm
from .models import CarMileageReport


def report_types(request):
    report_types = [
        {
            "name": "Отчет по пробегу автомобилей",
            "url": reverse_lazy("car_mileage_report"),
            "description": "Показывает пробег выбранного автомобиля за заданный период времени",
            "object_list": CarMileageReport.objects.all(),
        }
    ]
    context = {"report_types": report_types}
    return render(request, template_name="report/report_types.html", context=context)


# Create your views here.
@method_decorator(csrf_protect, name="dispatch")
class CarMileageReportView(LoginRequiredMixin, CreateView):
    template_name = "report/report_mileage_create.html"
    model = CarMileageReport
    context_object_name = "car_mileage_report"
    success_url = reverse_lazy("report_types")
    form_class = CarMileageReportForm
