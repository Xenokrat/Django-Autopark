import random
from datetime import datetime, timedelta
from math import atan2, cos, radians, sin, sqrt
from typing import Dict, List, Optional, Tuple, TypeVar, Union

import openrouteservice as ors  # type: ignore
import pytz
import requests
from django.conf import settings
from django.contrib.gis.geos.point import Point
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware

from auto.models import AutoRide, GPSData, Vehicle

Point_ = TypeVar("Point_", bound=Union[List[float], Tuple[float, float]])


class Command(BaseCommand):
    help = "Запускает движение авто по заданному маршруту между 2 точками"
    CITIES = [
        'Москва',
        'Рязань',
        'Брянск',
        'Смоленск',
        'Пенза',
        'Ярославь',
        'Нижний Новгород',
        'Тамбов',
        'Липецк',
        'Саранск',
        'Пенза',
    ]
    COORDS = [
        [37.615561, 55.741469],
        [39.752802, 54.608263],
        [33.728853, 53.091895],
        [32.770796, 54.758993],
        [45.025303, 53.197888],
        [41.5528, 44.4375],
        [41.618782, 52.670766],
        [39.590026, 52.607635],
        [45.224775, 54.191623],
        [45.025303, 53.197888],
    ]

    def _create_random_date(
        self,
        start_date_str: str,
        end_date_str: str
    ) -> datetime:
        format = "%Y-%m-%d:%H:%M:%S"
        start_date = datetime.strptime(start_date_str, format)
        end_date = datetime.strptime(end_date_str, format)
        random_date = start_date + (end_date - start_date) * random.random()
        return random_date

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client = ors.Client(key=settings.OPENROUTESERVISE_API)

    def add_arguments(self, parser) -> None:
        parser.add_argument("vehicle_id", type=int, help="ID автомобиля")
        parser.add_argument("count", type=int)

    def handle(self, *args, **options) -> None:
        self.vehicle_id = options["vehicle_id"]
        count = options["count"]

        enterprise = Vehicle.objects.get(pk=self.vehicle_id).enterprise
        if enterprise:
            self.tzinfo = pytz.timezone(enterprise.timezone)
        else:
            self.tzinfo = pytz.UTC

        for n in range(count):
            while True:
                self.start_address = random.choice(self.COORDS)
                self.end_address = random.choice(self.COORDS)
                while self.start_address == self.end_address:
                    self.end_address = random.choice(self.COORDS)

                start_point = self.start_address
                end_point = self.end_address

                # start_point = self.get_coordinates_from_address(
                #     self.start_address)
                # if start_point is None:
                #     CommandError(
                #         f"Начальный адрес не корректный {self.start_address}")
                #     continue
                #
                # end_point = self.get_coordinates_from_address(self.end_address)
                # if end_point is None:
                #     CommandError(
                #         f"Конечный адрес не корректный {self.end_address}")
                #     continue

                try:
                    coordinates = self.get_track(start_point, end_point)
                    break
                except ors.exceptions.ApiError:
                    continue

            self.vehicle_speed = random.randint(15, 30)

            self.timestamp: datetime = make_aware(self._create_random_date(
                '2020-01-01:00:00:00', '2023-01-01:00:00:00'))

            this_ride = AutoRide(
                vehicle_id=self.vehicle_id,
                start_date=self.timestamp,
                end_date=None,
                start_point=Point(*start_point),
                end_point=None,
                distance=0,
            )
            this_ride.save()

            self.current_speed: int = self.vehicle_speed
            self.start_time = self.timestamp

            # MAIN LOOP
            i = 0
            distance_p1_p2 = None
            total_distance = 0

            while i < len(coordinates) - 1:
                point_1 = coordinates[i]
                point_2 = coordinates[i + 1]

                distance_p1_p2 = self.distance_between_coordinates(
                    point_1, point_2)
                time_d = distance_p1_p2 / self.vehicle_speed
                self.timestamp += timedelta(seconds=time_d)
                self.write_point_to_base(point_2)
                total_distance += distance_p1_p2
                i += 1

            this_ride.end_point = Point(end_point)
            this_ride.end_date = self.timestamp
            this_ride.distance = round(total_distance / 1000, 2)
            this_ride.save()
            self.stdout.write(self.style.SUCCESS(
                f"{self.vehicle_id} -- success {n + 1}/{count}"))

    def get_coordinates_from_address(self, address: str) -> Optional[Point_]:
        endpoint_search = "https://api.openrouteservice.org/geocode/search"
        params: Dict[str, Union[int, str]] = {
            "api_key": settings.OPENROUTESERVISE_API,
            "text": address,
            "size": 1,
            "lang": "ru",
        }
        response = requests.get(endpoint_search, params=params)
        try:
            result = response.json()["features"][0]["geometry"]["coordinates"]
        except KeyError:
            return None
        except IndexError:
            return None

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
        a = (sin(d_lat / 2) ** 2) + cos(radians(lat1)) * \
            cos(radians(lat2)) * (sin(d_lon / 2) ** 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return round(distance, 2)

    def write_point_to_base(self, point_2: Point_) -> None:
        point = Point(*point_2)
        GPSData.objects.create(vehicle_id=self.vehicle_id,
                               point=point, timestamp=self.timestamp)
