import time
from datetime import datetime, timedelta
from math import atan2, cos, radians, sin, sqrt
from typing import Dict, List, Optional, Tuple, TypeVar, Union

import openrouteservice as ors  # type: ignore
import pytz
import requests
from django.conf import settings
from django.contrib.gis.geos.point import Point
from django.core.management.base import BaseCommand, CommandError

from auto.models import AutoRide, GPSData, Vehicle

Point_ = TypeVar("Point_", bound=Union[List[float], Tuple[float, float]])


class Command(BaseCommand):
    help = "Запускает движение авто по заданному маршруту между 2 точками"
    WRITE_TIME_OPTION = 1

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client = ors.Client(key=settings.OPENROUTESERVISE_API)
        self.current_speed: int = 0
        self.timestamp: datetime = datetime.now(tz=pytz.UTC)

    def add_arguments(self, parcer) -> None:
        parcer.add_argument("vehicle_id", type=int, help="ID автомобиля")
        parcer.add_argument("start_address", type=str, help="Начальный адрес поездки")
        parcer.add_argument("end_address", type=str, help="Конечный адрес поездки")
        parcer.add_argument("vehicle_speed", type=int, help="Скорость автомобиля")
        parcer.add_argument("vehicle_acceleration", type=int, help="Ускорение автомобиля")

    def handle(self, *args, **options) -> None:
        self.vehicle_id = options["vehicle_id"]
        self.start_address = options["start_address"]
        self.end_address = options["end_address"]
        self.vehicle_speed = options["vehicle_speed"]
        self.vehicle_acceleration = options["vehicle_acceleration"]

        enterprise = Vehicle.objects.get(pk=self.vehicle_id).enterprise
        if enterprise:
            self.tzinfo = pytz.timezone(enterprise.timezone)
        else:
            self.tzinfo = pytz.UTC
        self.start_time = self.timestamp

        start_point = self.get_coordinates_from_address(self.start_address)
        if start_point is None:
            CommandError("Начальный адрес не корректный")
            return

        end_point = self.get_coordinates_from_address(self.end_address)
        if end_point is None:
            CommandError("Конечный адрес не корректный")
            return

        this_ride = AutoRide(
            vehicle_id=self.vehicle_id,
            start_date=self.timestamp,
            end_date=None,
            start_point=Point(*start_point),
            end_point=None,
        )
        this_ride.save()

        self.stdout.write(
            self.style.SUCCESS(f"{self.timestamp} - Начата поездка из {self.start_address} в {self.end_address}")
        )
        coordinates = self.get_track(start_point, end_point)

        # MAIN LOOP
        i = 0
        distance_p1_p2 = None
        total_distance = 0

        while i < len(coordinates) - 1:
            point_1 = coordinates[i]
            point_2 = coordinates[i + 1]

            time.sleep(self.WRITE_TIME_OPTION)
            new_speed = self.WRITE_TIME_OPTION * self.vehicle_acceleration

            if new_speed > self.vehicle_speed:
                self.current_speed = self.vehicle_speed
                self.vehicle_acceleration = 0
            else:
                self.current_speed = new_speed

            vehicle_dist: int = (
                self.current_speed * self.WRITE_TIME_OPTION
                + self.vehicle_acceleration * (self.WRITE_TIME_OPTION**2) // 2
            )
            total_distance += vehicle_dist

            if not distance_p1_p2:
                distance_p1_p2 = self.distance_between_coordinates(point_1, point_2)

            if vehicle_dist < distance_p1_p2:
                distance_p1_p2 = distance_p1_p2 - vehicle_dist
                t: float = vehicle_dist / distance_p1_p2
                self.write_point_to_base(point_1, point_2, t)
                self.timestamp += timedelta(seconds=self.WRITE_TIME_OPTION)
                continue
            else:
                distance_p1_p2 = vehicle_dist - distance_p1_p2
                distance_p1_p2 = None
                i += 1
                continue

        this_ride.end_point = Point(end_point)
        this_ride.end_date = self.timestamp
        this_ride.save()

    def get_coordinates_from_address(self, address: str) -> Optional[Point_]:
        endpoint_search = "https://api.openrouteservice.org/geocode/search"
        params: Dict[str, Union[int, str]] = {
            "api_key": settings.OPENROUTESERVISE_API,
            "text": address,
            "size": 1,
            "lang": "ru",
        }
        response = requests.get(endpoint_search, params=params)
        result = response.json()["features"][0]["geometry"]["coordinates"]
        if result:
            return result
        return None

    def get_track(
        self,
        start_point: Point_,
        end_point: Point_,
    ) -> List[Point_]:
        route = self.client.directions(
            coordinates=([start_point] + [end_point]),
            profile="driving-car",
            format="geojson",
        )
        return route["features"][0]["geometry"]["coordinates"]

    @staticmethod
    def distance_between_coordinates(start: Point_, end: Point_):
        R = 6371000
        lon1, lat1 = start
        lon2, lat2 = end
        d_lat = radians(lat2 - lat1)
        d_lon = radians(lon2 - lon1)
        a = (sin(d_lat / 2) ** 2) + cos(radians(lat1)) * cos(radians(lat2)) * (sin(d_lon / 2) ** 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return round(distance, 2)

    def write_point_to_base(self, point_1: Point_, point_2: Point_, t: float) -> None:
        lat1, lon1 = point_1
        lat2, lon2 = point_2

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        lat = round(lat1 + delta_lat * t, 6)
        lon = round(lon1 + delta_lon * t, 6)
        point = Point(lat, lon)
        GPSData.objects.create(vehicle_id=self.vehicle_id, point=point, timestamp=self.timestamp)
        current_time = self.timestamp.replace(tzinfo=self.tzinfo).strftime("%Y-%m-%d: %H:%M")
        in_road = str(self.timestamp - self.start_time)
        self.stdout.write(
            self.style.SUCCESS(f"INFO: {current_time} записана точка - lat: {lat}, lon: {lon}, в пути {in_road}")
        )
