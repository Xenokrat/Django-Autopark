from django.http import HttpResponse
from django.urls import path

from .views import VehicleListView

urlpatterns = [
    path("", VehicleListView.as_view(), name="vehicles"),
]
