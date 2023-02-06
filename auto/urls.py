from django.http import HttpResponse
from django.urls import path

from .views import EnterpriseListView, LoginManagerView, VehicleListView

urlpatterns = [
    path("", EnterpriseListView.as_view(), name="home"),
    path("login/", LoginManagerView.as_view(), name="login"),
    path("vehicles/", VehicleListView.as_view(), name="vehicles"),
]
