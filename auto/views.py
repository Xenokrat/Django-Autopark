from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

from .models import Vehicle


@method_decorator(csrf_protect, name="dispatch")
class VehicleListView(ListView):
    template_name = "auto/vehicle_list.html"
    model = Vehicle
