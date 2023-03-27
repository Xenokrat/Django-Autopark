from copy import deepcopy
from datetime import datetime, timedelta

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import VehicleForm
from .models import AutoRide, Enterprise, GPSData, Vehicle


@method_decorator(csrf_protect, name="dispatch")
class VehicleListView(LoginRequiredMixin, ListView):
    template_name = "auto/vehicle_list.html"
    model = Vehicle
    # paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(enterprise=self.kwargs["pk"])


@method_decorator(csrf_protect, name="dispatch")
class VehicleDetailView(LoginRequiredMixin, DetailView):
    template_name = "auto/vehicle_detail.html"
    model = Vehicle
    context_object_name = "vehicle"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date = self.request.GET.get(
            "start_date", timezone.now().date() - timedelta(days=90))
        end_date = self.request.GET.get("end_date", timezone.now().date())
        print(start_date, end_date)

        auto_rides = AutoRide.objects.filter(vehicle=self.kwargs.get("pk"))
        # if start_date:
        #     auto_rides = auto_rides.filter(start_date__gte=start_date)
        #
        # if end_date:
        #     auto_rides = auto_rides.filter(end_date__lte=end_date)

        # timezone.activate(zoneinfo.ZoneInfo(tzname))
        context["auto_rides"] = auto_rides
        context["start_date"] = start_date
        context["end_date"] = end_date
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


@method_decorator(csrf_protect, name="dispatch")
class RideDetailView(LoginRequiredMixin, DetailView):
    template_name = "auto/ride_detail.html"
    model = AutoRide
    context_object_name = "ride"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.object.start_date
        if not start_date:
            start_date = "2000-01-01"

        end_date = self.object.end_date
        if not end_date:
            end_date = "2050-01-01"

        points = list(
            GPSData.objects.filter(Q(timestamp__range=(start_date, end_date)) & Q(
                vehicle=self.object.vehicle)).all()
        )
        points_list = [[p.point.x, p.point.y] for p in points[::60]]
        center_point = deepcopy(points_list[len(points_list) // 2])
        center_point[0], center_point[1] = center_point[1], center_point[0]
        geojson = {"type": "LineString", "coordinates": points_list}
        context["geo_points"] = geojson
        context["center_point"] = center_point
        return context
