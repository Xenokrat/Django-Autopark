import zoneinfo
from typing import Any

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import VehicleForm
from .models import Driver, Enterprise, Vehicle


@method_decorator(csrf_protect, name="dispatch")
class VehicleListView(LoginRequiredMixin, ListView):
    template_name = "auto/vehicle_list.html"
    model = Vehicle

    def get_queryset(self):
        return Vehicle.objects.filter(enterprise__in=self.request.user.manager.enterprise.all())


@method_decorator(csrf_protect, name="dispatch")
class VehicleDetailView(LoginRequiredMixin, DetailView):
    template_name = "auto/vehicle_detail.html"
    model = Vehicle
    context_object_name = "vehicle"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # tzname = self.object.enterprise.timezone
        # timezone.activate(zoneinfo.ZoneInfo(tzname))
        return context


@method_decorator(csrf_protect, name="dispatch")
class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "auto/vehicle_update.html"
    model = Vehicle
    context_object_name = "vehicle"
    form_class = VehicleForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["manager"] = self.request.user.manager
        return kwargs

    def form_valid(self, form):
        vehicle = form.save()
        self.pk = vehicle.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicle", kwargs={"pk": self.pk})


@method_decorator(csrf_protect, name="dispatch")
class VehicleCreateView(LoginRequiredMixin, CreateView):
    template_name = "auto/vehicle_create.html"
    model = Vehicle
    context_object_name = "vehicle"
    form_class = VehicleForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["manager"] = self.request.user.manager
        return kwargs

    def form_valid(self, form):
        vehicle = form.save()
        self.pk = vehicle.enterprise.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicles")


@method_decorator(csrf_protect, name="dispatch")
class VehicleDeleteView(LoginRequiredMixin, DeleteView):  # type: ignore
    template_name = "auto/vehicle_delete.html"
    model = Vehicle
    context_object_name = "vehicle"
    success_url = reverse_lazy("vehicles")


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


def user_logout(request):
    logout(request)
    return redirect("login")
