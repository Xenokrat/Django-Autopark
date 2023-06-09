from datetime import datetime, timedelta

from django.contrib.gis.geos import LineString, Point
from django.core.management.base import BaseCommand, CommandError

from auto.models import GPSData, Vehicle


class Command(BaseCommand):
    moscow = Point(43.816, 55.3767, srid=4326)
    tver = Point(43.9242, 56.3157, srid=4326)

    ride_start = datetime(2023, 1, 20, 12, 0, 0)
    time_step = 10
    ride_duration = 2 * 60 * 60  # 2 hours
    num_points = int(ride_duration / time_step)

    def add_arguments(self, parser):
        parser.add_argument("vehicle", type=str)

    def handle(self, *args, **options):
        vehicle_arg = options.get("vehicle")
        if not vehicle_arg:
            raise CommandError("Не предоставлен id автомобиля")

        vehicle = Vehicle.objects.get(pk=vehicle_arg)

        line = LineString([self.moscow, self.tver])

        for i in range(self.num_points):
            time = self.ride_start + timedelta(seconds=i * self.time_step)
            point = line.interpolate(float(i) / self.num_points)
            GPSData.objects.create(
                vehicle=vehicle,
                timestamp=time,
                point=point,
            )

        self.stdout.write(self.style.SUCCESS("Успешно добавлены GPS данные"))
