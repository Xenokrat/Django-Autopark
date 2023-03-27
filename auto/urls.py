from django.urls import path

from .views import (EnterpriseListView, LoginManagerView, RideDetailView,
                    VehicleCreateView, VehicleDeleteView, VehicleDetailView,
                    VehicleListView, VehicleUpdateView, user_logout)

urlpatterns = [
    path("", EnterpriseListView.as_view(), name="home"),
    path("login/", LoginManagerView.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
    path("vehicles/<int:pk>/",
         VehicleListView.as_view(), name="vehicles"),
    path("vehicle/<int:pk>/", VehicleDetailView.as_view(), name="vehicle"),
    path("vehicle/<int:pk>/update/",
         VehicleUpdateView.as_view(), name="vehicle_update"),
    path("vehicle/create/", VehicleCreateView.as_view(), name="vehicle_create"),
    path("vehicle/<int:pk>/delete/",
         VehicleDeleteView.as_view(), name="vehicle_delete"),
    path("ride/<int:pk>/", RideDetailView.as_view(), name="ride"),
]
