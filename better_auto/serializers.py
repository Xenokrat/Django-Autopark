from rest_framework import serializers

from .models import BetterVehicle
from .service import VehicleService

vehicle_service = VehicleService()


class BetterVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetterVehicle
        fields = (
            "registration_number",
            "year",
            "cost",
            "brand",
            "enterprise",
            "driver",
        )

    def validate(self, data):
        vehicle_service._validate_and_processed_vehicle(data)
        return data
