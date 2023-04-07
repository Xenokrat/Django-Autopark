from abc import ABC, abstractmethod

from django.db.models import QuerySet

from .models import BetterBrand, BetterDriver, BetterEnterprise, BetterVehicle


class AbstractVehicleRepository(ABC):
    @abstractmethod
    def get_all_vehicles(self) -> QuerySet[BetterVehicle]:
        pass

    @abstractmethod
    def get_vehicle_by_id(self, item_id: int) -> BetterVehicle:
        pass


class VehicleRepository(AbstractVehicleRepository):
    def get_all_vehicles(self) -> QuerySet:
        return BetterVehicle.objects.all()

    def get_vehicle_by_id(self, item_id: int) -> BetterVehicle:
        return BetterVehicle.objects.get(item_id)


class AbstractDriverRepository(ABC):
    @abstractmethod
    def get_all_drivers(self) -> QuerySet:
        pass

    @abstractmethod
    def get_driver_by_id(self, item_id: int) -> BetterDriver:
        pass


class DriverRepository(AbstractDriverRepository):
    def get_all_drivers(self) -> QuerySet[BetterDriver]:
        return BetterDriver.objects.all()

    def get_driver_by_id(self, item_id: int) -> BetterDriver:
        return BetterDriver.objects.get(item_id)


class AbstractBrandRepository(ABC):
    @abstractmethod
    def get_all_brands(self) -> QuerySet[BetterBrand]:
        pass

    @abstractmethod
    def get_brand_by_id(self, item_id: int) -> BetterBrand:
        pass


class BrandRepository(AbstractBrandRepository):
    def get_all_brands(self) -> QuerySet[BetterBrand]:
        return BetterBrand.objects.all()

    def get_brand_by_id(self, item_id: int) -> BetterBrand:
        return BetterBrand.objects.get(item_id)


class AbstractEnterpriseRepository(ABC):
    @abstractmethod
    def get_all_enterprises(self) -> QuerySet[BetterEnterprise]:
        pass

    @abstractmethod
    def get_enterprise_by_id(self, item_id: int) -> BetterEnterprise:
        pass


class EnterpriseRepository(AbstractEnterpriseRepository):
    def get_all_enterprises(self) -> QuerySet[BetterEnterprise]:
        return BetterEnterprise.objects.all()

    def get_enterprise_by_id(self, item_id: int) -> BetterEnterprise:
        return BetterEnterprise.objects.get(item_id)
