from django.urls import path

from . import views

urlpatterns = [
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("vehicles/<int:pk>/", views.vehicle_detail, name="vehicle_detail"),
    path("drivers/", views.driver_list, name="driver_list"),
    path("drivers/<int:pk>/", views.driver_detail, name="driver_detail"),
    path("enterprises/", views.enterprise_list, name="enterprises_list"),
    path("enterprises/<int:pk>/", views.enterprise_detail, name="enterprises_detail"),
]
