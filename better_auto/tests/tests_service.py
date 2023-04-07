from django.test import TestCase
from django.urls import reverse

from better_auto.models import BetterBrand, BetterEnterprise, BetterVehicle
from better_auto.service import VehicleService


class VehicleServiceTest(TestCase):
    def setUp(self):
        self.vehicle_service = VehicleService()
        self.enterprise1 = BetterEnterprise.objects.create(
            name="Ent1",
            city="Moscow",
            timezone="Europe/Moscow",
        )
        self.enterprise2 = BetterEnterprise.objects.create(
            name="Ent2",
            city="Kaliningrad",
            timezone="UTC",
        )
        self.brand1 = BetterBrand(brand="Lada")
        self.brand2 = BetterBrand(brand="Reno")

        self.vehicle1 = BetterVehicle(
            registration_number="AAAAAA",
            year=1984,
            cost=100000.00,
            brand=self.brand1,
            enterprise=self.enterprise1,
        )

        self.vehicle2 = BetterVehicle(
            registration_number="BBBBBB",
            year=2010,
            cost=1000.50,
            brand=self.brand2,
            enterprise=self.enterprise2,
        )

    def test_get_all_vehicles(self):
        vehicles = self.vehicle_service.get_all_vehicles()
        self.assertEqual(len(vehicles), 2)
        self.assertEqual(vehicles[0]["brand"], self.vehicle1.brand)
        self.assertEqual(vehicles[1]["brand"], self.vehicle2.brand)
        self.assertEqual(vehicles[0]["enterprise"], self.vehicle1.enterprise)
        self.assertEqual(vehicles[1]["enterprise"], self.vehicle2.enterprise)

    def test_get_vehicle_by_id(self):
        vehicle = self.vehicle_service.get_vehicle_by_id(self.vehicle1.pk)
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle["brand"], self.vehicle1.brand)
        self.assertEqual(vehicle["enterprise"], self.vehicle1.enterprise)

        vehicle = self.vehicle_service.get_vehicle_by_id(self.vehicle2.pk)
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle["brand"], self.vehicle2.brand)
        self.assertEqual(vehicle["enterprise"], self.vehicle2.enterprise)

        vehicle = self.vehicle_service.get_car_by_id(99999)
        self.assertIsNone(vehicle)
