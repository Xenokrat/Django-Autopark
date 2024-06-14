from django.urls import path

from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

from . import views

schema_view = get_schema_view(
    openapi.Info( title="Автопарк API", default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("vehicles/<int:pk>/", views.vehicle_detail, name="vehicle_detail"),
    path("drivers/", views.driver_list, name="driver_list"),
    path("drivers/<int:pk>/", views.driver_detail, name="driver_detail"),
    path("enterprises/", views.enterprise_list, name="enterprises_list"),
    path("gps-data/", views.gps_data_set, name="gps_auto_data"),
    path("auto-rides/vehicle/<int:pk>/", views.auto_rides_set, name="auto_rides_set"),
    path("auto-rides/rides/vehicle/<int:pk>/", views.auto_rides_list, name="auto_rides_list"),
    path("reports/car-mil-report/<int:pk>/", views.car_mileage_report, name="car_miliage_report_api"),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
