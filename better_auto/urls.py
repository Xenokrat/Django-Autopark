from django.urls import path

from . import views

urlpatterns = [
    path("better-vehicles/", views.vehicle_list, name="better_vehicles_list"),
    path("better-vehicles/<int:id>", views.vehicle_detail, name="better_vehicle_detail"),
]
