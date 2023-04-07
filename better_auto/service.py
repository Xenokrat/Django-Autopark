import re
from typing import Optional

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from .models import BetterVehicle
from .repository import (DriverRepository, EnterpriseRepository,
                         VehicleRepository)


class VehicleService:
    def __init__(self) -> None:
        self.vehicle_repository = VehicleRepository()
        self.driver_repository = DriverRepository()
        self.enterprise_repository = EnterpriseRepository()

    def get_all_vehicles(self) -> QuerySet[BetterVehicle]:
        vehicles = self.vehicle_repository.get_all_vehicles()
        map(self._validate_and_processed_vehicle, vehicles)
        return vehicles

    def get_vehicle_by_id(self, vehicle_id: int) -> BetterVehicle:
        vehicle = self.vehicle_repository.get_vehicle_by_id(vehicle_id)
        self._validate_and_processed_vehicle(vehicle)
        return vehicle

    def _validate_vehicle_driver(self, vehicle_id: int, driver_id: int) -> bool:
        vehicle = self.vehicle_repository.get_vehicle_by_id(vehicle_id)
        driver = self.driver_repository.get_driver_by_id(driver_id)
        enterprise = self.enterprise_repository.get_enterprise_by_id(vehicle.enterprise_id)

        if vehicle is None or driver is None or enterprise is None:
            return False

        return driver.enterprise_id == enterprise.id

    def _validate_reg_numbers(self, vehicle_id: int) -> bool:
        regex = "^\w*$"
        reg_number = self.vehicle_repository.get_vehicle_by_id(vehicle_id).registration_number
        if not reg_number:
            return False
        if not re.search(regex, reg_number):
            return False
        return True

    def _validate_and_processed_vehicle(self, vehicle: Optional[BetterVehicle]) -> None:
        if vehicle is None:
            return None
        if not all(
            [
                self._validate_reg_numbers(vehicle.id),
                self._validate_vehicle_driver(vehicle.driver_id, vehicle.enterprise_id),
            ]
        ):
            raise ValidationError("Not valid")
