from django import forms

from .models import Driver, Enterprise, Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "model",
            "registration_number",
            "VIN",
            "year",
            "cost",
            "mileage",
            "color",
            "purchase_date",
            "current_driver",
            "enterprise",
        ]
        widgets = {
            "model": forms.Select(attrs={"class": "form-control"}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "VIN": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "cost": forms.NumberInput(attrs={"class": "form-control"}),
            "mileage": forms.NumberInput(attrs={"class": "form-control"}),
            "purchase_date": forms.DateInput(attrs={"class": "form-control"}),
            "enterprise": forms.Select(attrs={"class": "form-control"}),
            "current_driver": forms.Select(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop("manager", None)
        super().__init__(*args, **kwargs)
        if manager:
            self.fields["enterprise"].queryset = Enterprise.objects.filter(manager=manager)
            self.fields["current_driver"].queryset = Driver.objects.filter(enterprise__in=manager.enterprise.all())
