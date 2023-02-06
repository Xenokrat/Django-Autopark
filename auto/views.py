from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

from .models import Enterprise, Vehicle


@method_decorator(csrf_protect, name="dispatch")
class VehicleListView(LoginRequiredMixin, ListView):
    template_name = "auto/vehicle_list.html"
    model = Vehicle


@method_decorator(csrf_protect, name="dispatch")
class EnterpriseListView(LoginRequiredMixin, ListView):
    template_name = "auto/enterprise_list.html"
    model = Enterprise

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        if hasattr(self.request.user, "manager"):
            return qs.filter(manager=self.request.user.manager)
        return qs.none()


@method_decorator(csrf_protect, name="dispatch")
class LoginManagerView(LoginView):
    template_name = "auto/registration/login_manager.html"
