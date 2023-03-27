from django import forms

from .models import CarMileageReport


class DateInput(forms.DateInput):
    input_type = "date"


class CarMileageReportForm(forms.ModelForm):
    class Meta:
        model = CarMileageReport
        fields = [
            "vehicle",
            "period",
            "start_date",
            "end_date",
            "report_type",
        ]
        widgets = {
            "vehicle": forms.Select(attrs={"class": "form-control"}),
            "period": forms.Select(attrs={"class": "form-control"}),
            "start_date": DateInput,
            "end_date": DateInput,
            "cost": forms.NumberInput(attrs={"class": "form-control"}),
        }
